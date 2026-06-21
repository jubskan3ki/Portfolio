"""Taches Celery pour les webhooks."""

import logging
import uuid
from typing import Any

from celery import shared_task
from django.db import DatabaseError, OperationalError

logger = logging.getLogger(__name__)


@shared_task(
    max_retries=3,
    name="webhooks.dispatch_event",
    autoretry_for=(OperationalError,),
    retry_backoff=True,
)
def dispatch_webhook_event(
    event_type: str, payload: dict[str, Any], event_id: str | None = None
) -> dict[str, Any]:
    """Cree les livraisons d'un evenement puis fan-out l'envoi HTTP.

    Cette tache ne fait que du travail DB (creation des livraisons PENDING) puis
    enfile une tache `send_webhook_delivery` par livraison : un endpoint lent ou
    en echec n'impacte plus les autres, et aucune tache n'accumule N envois HTTP
    sequentiels (risque de soft_time_limit). Le retry (erreurs DB transitoires)
    est gere par autoretry_for, sans self.retry.

    Args:
        event_type: Type d'evenement
        payload: Donnees de l'evenement
        event_id: UUID string pour la deduplication

    Returns:
        Statistiques de dispatch
    """
    from .models import Webhook
    from .services import WebhookDispatcher

    # Idempotency: skip if no active webhooks for this event
    if not Webhook.objects.active().exists():
        logger.info("No active webhooks, skipping dispatch for: %s", event_type)
        return {"event_type": event_type, "total_deliveries": 0, "skipped": True}

    parsed_event_id = uuid.UUID(event_id) if event_id else None

    deliveries = WebhookDispatcher.create_deliveries(event_type, payload, event_id=parsed_event_id)

    for delivery in deliveries:
        send_webhook_delivery.delay(str(delivery.pk))

    logger.info(
        "Webhook event dispatched: %s (%d deliveries enqueued)",
        event_type,
        len(deliveries),
    )
    return {
        "event_type": event_type,
        "total_deliveries": len(deliveries),
        "dispatched": True,
    }


@shared_task(
    name="webhooks.send_delivery",
    autoretry_for=(OperationalError,),
    retry_backoff=True,
    max_retries=3,
)
def send_webhook_delivery(delivery_id: str) -> dict[str, Any]:
    """Envoie une seule livraison de webhook (envoi HTTP isole).

    L'echec reseau n'est PAS retente ici : `send_delivery` marque la livraison
    RETRYING avec son `next_retry_at` (backoff), et la tache periodique la
    reprend. On retente uniquement les erreurs DB transitoires (verrou DB, etc.).

    Args:
        delivery_id: PK de la WebhookDelivery a envoyer

    Returns:
        Resultat de l'envoi
    """
    from .models import WebhookDelivery
    from .services import WebhookDispatcher

    try:
        delivery = WebhookDelivery.objects.select_related("webhook").get(pk=delivery_id)
    except WebhookDelivery.DoesNotExist:
        logger.warning("Webhook delivery introuvable: %s", delivery_id)
        return {"delivery_id": delivery_id, "found": False}

    if delivery.status == WebhookDelivery.Status.SUCCESS:
        return {"delivery_id": delivery_id, "skipped": "already_success"}

    if not delivery.webhook.is_active:
        return {"delivery_id": delivery_id, "skipped": "inactive"}

    success = WebhookDispatcher.send_delivery(delivery)
    return {"delivery_id": delivery_id, "success": success}


@shared_task(name="webhooks.retry_failed_deliveries")
def retry_failed_webhook_deliveries() -> dict[str, int]:
    """Enfile le re-envoi des livraisons echouees dues (fan-out par livraison).

    Cette tache devrait etre executee periodiquement (ex: toutes les 5 minutes).

    Returns:
        Nombre de livraisons enfilees
    """
    from utils.locks import single_run_lock

    from .services import WebhookDispatcher

    # TTL < intervalle Beat (300s) : evite tout chevauchement entre deux runs.
    with single_run_lock("webhooks.retry_failed_deliveries", 290) as acquired:
        if not acquired:
            logger.info("Retry deja en cours, run ignore")
            return {"retried_count": 0, "skipped": True}
        try:
            count = WebhookDispatcher.enqueue_due_retries()
            logger.info("Enqueued %d webhook deliveries for retry", count)
            return {"retried_count": count}
        except (DatabaseError, OperationalError):
            logger.exception("Failed to enqueue webhook delivery retries")
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

    from utils.locks import single_run_lock

    from .models import WebhookDelivery

    with single_run_lock("webhooks.cleanup_old_deliveries", 3600) as acquired:
        if not acquired:
            logger.info("Cleanup webhooks deja en cours, run ignore")
            return {"deleted_count": 0, "skipped": True}

        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count, _ = WebhookDelivery.objects.filter(
            created_at__lt=cutoff_date,
        ).delete()

        logger.info("Cleaned up %d old webhook deliveries", deleted_count)
        return {"deleted_count": deleted_count}
