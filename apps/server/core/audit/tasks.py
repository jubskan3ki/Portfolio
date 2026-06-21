"""Taches Celery pour la maintenance des audit logs."""

import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

DEFAULT_RETENTION_DAYS = 180


@shared_task(name="audit.cleanup_old_logs")
def cleanup_old_audit_logs(days: int | None = None) -> dict[str, int]:
    """Supprime les audit logs plus vieux que `days` jours.

    Args:
        days: Nombre de jours a conserver. Defaut = settings.AUDIT_LOG_RETENTION_DAYS
              ou 180 jours.

    Returns:
        dict avec deleted_count.
    """
    from utils.locks import single_run_lock

    from core.audit.models import AuditLog

    retention = days if days is not None else getattr(settings, "AUDIT_LOG_RETENTION_DAYS", DEFAULT_RETENTION_DAYS)

    with single_run_lock("audit.cleanup_old_logs", 3600) as acquired:
        if not acquired:
            logger.info("Cleanup audit logs deja en cours, run ignore")
            return {"deleted_count": 0, "retention_days": retention, "skipped": True}

        cutoff = timezone.now() - timedelta(days=retention)
        deleted_count, _ = AuditLog.objects.filter(timestamp__lt=cutoff).delete()
        logger.info("Cleaned up %d audit logs older than %d days", deleted_count, retention)
        return {"deleted_count": deleted_count, "retention_days": retention}
