"""Managers pour les modeles de statistiques."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from django.db import models
from django.db.models import Avg, Count, QuerySet
from django.utils import timezone

if TYPE_CHECKING:
    from core.stats.models import ViewLog, WebVitalEvent

logger = logging.getLogger("core.stats")


class ViewLogManager(models.Manager["ViewLog"]):
    """Manager pour le modele ViewLog."""

    def log_view(self, content_type: str, content_id: int) -> Any:
        """Enregistre une vue pour un contenu.

        Incremente le compteur si une entree existe deja pour aujourd'hui,
        sinon cree une nouvelle entree.
        """
        today = timezone.now().date()
        obj, created = self.get_or_create(
            content_type=content_type,
            content_id=content_id,
            viewed_at=today,
            defaults={"count": 1},
        )
        if not created:
            # F() = increment atomique SQL sans refresh_from_db (eviter un SELECT sur ce chemin chaud).
            obj.count = models.F("count") + 1
            obj.save(update_fields=["count"])
        logger.debug(
            "ViewLog: type=%s, id=%s, created=%s",
            content_type,
            content_id,
            created,
        )
        return obj


class WebVitalEventManager(models.Manager["WebVitalEvent"]):
    """Manager pour les evenements Web Vitals."""

    def for_metric(self, metric_name: str) -> QuerySet[WebVitalEvent]:
        """Filtre les evenements par nom de metrique."""
        return self.get_queryset().filter(metric_name=metric_name)

    def for_path(self, path: str) -> QuerySet[WebVitalEvent]:
        """Filtre les evenements par chemin de page."""
        return self.get_queryset().filter(path=path)

    def recent(self, days: int = 7) -> QuerySet[WebVitalEvent]:
        """Retourne les evenements des N derniers jours."""
        threshold = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(created_at__gte=threshold)

    def summary_by_metric(self, days: int = 7) -> QuerySet:
        """Retourne les statistiques agregees par metrique sur N jours.

        Retourne: metric_name, count, avg_value pour chaque metrique.
        """
        threshold = timezone.now() - timedelta(days=days)
        return (
            self.get_queryset()
            .filter(created_at__gte=threshold)
            .values("metric_name")
            .annotate(
                count=Count("id"),
                avg_value=Avg("value"),
            )
            .order_by("metric_name")
        )
