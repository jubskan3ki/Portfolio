"""Service pour la validation et normalisation des Web Vitals."""

import logging
from typing import Any

from utils.exceptions.service import ValidationError

logger = logging.getLogger("core.stats")


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
