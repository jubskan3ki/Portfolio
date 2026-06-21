"""Service pour la validation et normalisation des Web Vitals."""

import logging
from datetime import timedelta
from statistics import fmean
from typing import TYPE_CHECKING, Any

from django.utils import timezone

from utils.exceptions.service import ValidationError

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from ..models import WebVitalEvent

logger = logging.getLogger("core.stats")


def _percentile(values: list[float], percentile: int) -> float | None:
    """Calcule un percentile simple sur une liste triee."""
    if not values:
        return None

    sorted_values = sorted(values)
    index = round((len(sorted_values) - 1) * (percentile / 100))
    return float(sorted_values[index])


class WebVitalsService:
    """Logique metier de validation/normalisation des metriques Web Vitals."""

    ALLOWED_VIEWPORT_KEYS = {"width", "height"}

    @staticmethod
    def validate_metric_value(value: float) -> float:
        """Verifie que la valeur de la metrique est >= 0."""
        if value < 0:
            raise ValidationError("La metrique 'value' ne peut pas etre negative.")
        return value

    @staticmethod
    def validate_metric_delta(delta: float) -> float:
        """Verifie que le delta est >= 0."""
        if delta < 0:
            raise ValidationError("La metrique 'delta' ne peut pas etre negative.")
        return delta

    @classmethod
    def normalize_viewport(cls, viewport: dict[str, Any]) -> dict[str, int]:
        """Valide et normalise les dimensions viewport.

        - Coercition en int
        - Verification que les valeurs sont positives
        - Suppression des cles non autorisees
        """
        if not viewport:
            return {}

        extra_keys = set(viewport.keys()) - cls.ALLOWED_VIEWPORT_KEYS
        if extra_keys:
            raise ValidationError("Le champ 'viewport' ne supporte que 'width' et 'height'.")

        normalized: dict[str, int] = {}
        for key in cls.ALLOWED_VIEWPORT_KEYS:
            raw = viewport.get(key)
            if raw is None:
                continue
            try:
                numeric_value = int(raw)
            except (TypeError, ValueError) as exc:
                raise ValidationError(f"Le champ viewport.{key} doit etre un entier.") from exc
            if numeric_value <= 0:
                raise ValidationError(f"Le champ viewport.{key} doit etre positif.")
            normalized[key] = numeric_value

        return normalized

    @classmethod
    def ingest(cls, payload: dict[str, Any]) -> None:
        """Persiste un evenement Web Vitals valide.

        Args:
            payload: Donnees validees par le serializer.
        """
        from ..models import WebVitalEvent

        viewport = payload.get("viewport", {})
        WebVitalEvent.objects.create(
            metric_name=payload["name"],
            value=payload["value"],
            rating=payload["rating"],
            delta=payload.get("delta", 0),
            metric_id=payload["id"],
            path=payload["page"],
            full_url=payload.get("url", ""),
            user_agent=payload.get("userAgent", "")[:512],
            language=payload.get("language"),
            viewport_width=viewport.get("width"),
            viewport_height=viewport.get("height"),
            connection_type=payload.get("connectionType"),
            is_mobile=payload.get("isMobile"),
        )
        logger.debug("Web Vital ingested: %s", payload["name"])

    @staticmethod
    def _summarize_queryset(queryset: "QuerySet[WebVitalEvent]") -> list[dict]:
        """Agrege count / mean / percentiles / ratings par metrique.

        Les percentiles utilisent le rang le plus proche (_percentile) pour rester
        coherents avec la commande aggregate_web_vitals et le collector Prometheus.
        """
        grouped_values: dict[str, list[float]] = {}
        grouped_ratings: dict[str, dict[str, int]] = {}
        for metric_name, value, rating in queryset.values_list("metric_name", "value", "rating"):
            grouped_values.setdefault(metric_name, []).append(float(value))
            ratings = grouped_ratings.setdefault(metric_name, {"good": 0, "needs-improvement": 0, "poor": 0})
            if rating in ratings:
                ratings[rating] += 1

        return [
            {
                "metric_name": metric_name,
                "count": len(values),
                "mean": round(float(fmean(values)), 2) if values else None,
                "p75": _percentile(values, 75),
                "p95": _percentile(values, 95),
                "ratings": grouped_ratings[metric_name],
            }
            for metric_name, values in sorted(grouped_values.items())
        ]

    @classmethod
    def summary(cls, days: int) -> dict:
        """Construit la synthese agregee des Web Vitals sur une fenetre glissante.

        Args:
            days: Nombre de jours de la fenetre glissante (deja valide par la vue).

        Returns:
            Dictionnaire pret a serialiser : window_days, total_events, metrics.
        """
        from ..models import WebVitalEvent

        since = timezone.now() - timedelta(days=days)
        metrics_summary = cls._summarize_queryset(WebVitalEvent.objects.filter(created_at__gte=since))

        return {
            "window_days": days,
            "total_events": sum(metric["count"] for metric in metrics_summary),
            "metrics": metrics_summary,
        }
