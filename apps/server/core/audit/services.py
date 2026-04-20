"""Services analytiques pour les audit logs."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone

from core.audit.models import AuditLog

DEFAULT_STATS_WINDOW_DAYS = 30
DEFAULT_TOP_N = 10


def compute_stats(
    window_days: int = DEFAULT_STATS_WINDOW_DAYS,
    top_n: int = DEFAULT_TOP_N,
) -> dict[str, Any]:
    """Agrege les statistiques d'audit sur la fenetre demandee.

    Returns:
        Dict avec total, by_action, top_models, top_users, activity_per_day.
    """
    since = timezone.now() - timedelta(days=window_days)
    base_qs = AuditLog.objects.filter(timestamp__gte=since)

    total = base_qs.count()

    by_action = {row["action"]: row["count"] for row in base_qs.values("action").annotate(count=Count("id"))}

    top_models = list(base_qs.values("model_name").annotate(count=Count("id")).order_by("-count")[:top_n])

    top_users = list(
        base_qs.exclude(user=None).values("user__email").annotate(count=Count("id")).order_by("-count")[:top_n]
    )

    activity_per_day = list(
        base_qs.annotate(day=TruncDay("timestamp")).values("day").annotate(count=Count("id")).order_by("day")
    )

    return {
        "window_days": window_days,
        "total": total,
        "by_action": by_action,
        "top_models": top_models,
        "top_users": top_users,
        "activity_per_day": activity_per_day,
    }


def get_object_timeline(model_name: str, object_id: str) -> list[AuditLog]:
    """Retourne l'historique complet d'un objet (tous les audit logs)."""
    return list(AuditLog.objects.for_object(model_name, object_id).order_by("-timestamp"))
