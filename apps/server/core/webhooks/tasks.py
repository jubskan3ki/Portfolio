"""Taches Celery pour les webhooks."""

import logging
import uuid
from typing import Any

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    name="webhooks.dispatch_event",
)
def dispatch_webhook_event(
    self, event_type: str, payload: dict[str, Any], event_id: str | None = None
) -> dict[str, Any]:
    """Dispatch un evenement webhook de maniere asynchrone.

    Args:
        event_type: Type d'evenement
        payload: Donnees de l'evenement
        event_id: UUID string pour la deduplication

    Returns:
        Statistiques de livraison
    """
    from .models import Webhook
    from .services import WebhookDispatcher

    # Idempotency: skip if no active webhooks for this event
    if not Webhook.objects.active().exists():
        logger.info("No active webhooks, skipping dispatch for: %s", event_type)
        return {"event_type": event_type, "total_deliveries": 0, "skipped": True}

    parsed_event_id = uuid.UUID(event_id) if event_id else None

    try:
        deliveries = WebhookDispatcher.dispatch(event_type, payload, event_id=parsed_event_id)
        success_count = sum(1 for d in deliveries if d.status == "success")
        failed_count = len(deliveries) - success_count

        logger.info(
            "Webhook event dispatched: %s (success=%d, failed=%d)",
            event_type,
            success_count,
            failed_count,
        )

        return {
            "event_type": event_type,
            "total_deliveries": len(deliveries),
            "success_count": success_count,
            "failed_count": failed_count,
        }
    except (ConnectionError, TimeoutError, OSError) as e:
        logger.exception("Network error dispatching webhook event: %s", event_type)
        raise self.retry(exc=e, countdown=60 * (2**self.request.retries)) from e


@shared_task(name="webhooks.retry_failed_deliveries")
def retry_failed_webhook_deliveries() -> dict[str, int]:
    """Retente les livraisons de webhooks echouees.

    Cette tache devrait etre executee periodiquement (ex: toutes les 5 minutes).

    Returns:
        Nombre de livraisons retentees
    """
    from .services import WebhookDispatcher

    try:
        count = WebhookDispatcher.retry_failed_deliveries()
        logger.info("Retried %d failed webhook deliveries", count)
        return {"retried_count": count}
    except (ConnectionError, TimeoutError, OSError):
        logger.exception("Failed to retry webhook deliveries")
        return {"retried_count": 0, "error": True}


@shared_task(name="webhooks.cleanup_old_deliveries")
def cleanup_old_webhook_deliveries(days: int = 30) -> dict[str, int]:
    """Nettoie les anciennes livraisons de webhooks.

    Args:
        days: Nombre de jours a conserver

    Returns:
        Nombre de livraisons supprimees
    """
    from datetime import timedelta

    from django.utils import timezone

    from .models import WebhookDelivery

    cutoff_date = timezone.now() - timedelta(days=days)
    deleted_count, _ = WebhookDelivery.objects.filter(
        created_at__lt=cutoff_date,
    ).delete()

    logger.info("Cleaned up %d old webhook deliveries", deleted_count)
    return {"deleted_count": deleted_count}
