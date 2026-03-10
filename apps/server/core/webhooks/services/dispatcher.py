"""Services pour le systeme de webhooks."""

import json
import logging
import time
import uuid
from datetime import timedelta
from typing import Any

import requests
from django.db import models
from django.utils import timezone

from ..models import Webhook, WebhookDelivery

logger = logging.getLogger(__name__)


class WebhookDispatcher:
    """Service pour dispatcher les webhooks."""

    TIMEOUT = (5, 10)  # (connect_timeout, read_timeout) en secondes
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Portfolio-Webhook/1.0",
    }

    @classmethod
    def dispatch(
        cls,
        event_type: str,
        payload: dict[str, Any],
        event_id: uuid.UUID | None = None,
    ) -> list[WebhookDelivery]:
        """Dispatch un evenement a tous les webhooks abonnes.

        Args:
            event_type: Type d'evenement (ex: article.created)
            payload: Donnees de l'evenement
            event_id: UUID pour la deduplication (genere si absent)

        Returns:
            Liste des livraisons creees
        """
        if event_id is None:
            event_id = uuid.uuid4()

        webhooks = list(Webhook.objects.for_event(event_type))
        deliveries = []

        # Deduplication batch : une seule requete pour tous les webhooks
        already_delivered = set(
            WebhookDelivery.objects.filter(webhook__in=webhooks, event_id=event_id).values_list("webhook_id", flat=True)
        )

        for webhook in webhooks:
            if webhook.pk in already_delivered:
                logger.info(
                    "Webhook delivery skipped (duplicate): %s -> %s (event_id=%s)",
                    event_type,
                    webhook.name,
                    event_id,
                )
                continue

            delivery = cls._create_delivery(webhook, event_type, payload, event_id)
            deliveries.append(delivery)
            cls.send_delivery(delivery)

        return deliveries

    @classmethod
    def dispatch_async(cls, event_type: str, payload: dict[str, Any]) -> None:
        """Dispatch un evenement de maniere asynchrone via Celery.

        Args:
            event_type: Type d'evenement
            payload: Donnees de l'evenement
        """
        from ..tasks import dispatch_webhook_event

        dispatch_webhook_event.delay(event_type, payload, str(uuid.uuid4()))

    @classmethod
    def _create_delivery(
        cls,
        webhook: Webhook,
        event_type: str,
        payload: dict[str, Any],
        event_id: uuid.UUID,
    ) -> WebhookDelivery:
        """Cree un enregistrement de livraison."""
        return WebhookDelivery.objects.create(
            webhook=webhook,
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            status=WebhookDelivery.Status.PENDING,
        )

    @classmethod
    def _mark_delivery_success(
        cls,
        delivery: WebhookDelivery,
        response_status: int,
        response_body: str,
        duration_ms: int,
    ) -> None:
        """Marque une livraison comme reussie et met a jour les stats du webhook."""
        delivery.status = WebhookDelivery.Status.SUCCESS
        delivery.response_status = response_status
        delivery.response_body = response_body[:1000]
        delivery.delivered_at = timezone.now()
        delivery.duration_ms = duration_ms
        delivery.save(
            update_fields=[
                "status",
                "response_status",
                "response_body",
                "delivered_at",
                "duration_ms",
            ]
        )
        cls._increment_webhook_stats(delivery.webhook, success=True)

    @classmethod
    def _mark_delivery_failed(
        cls,
        delivery: WebhookDelivery,
        response_status: int | None,
        response_body: str,
        duration_ms: int,
    ) -> None:
        """Marque une livraison comme echouee avec backoff exponentiel."""
        delivery.attempts += 1
        delivery.response_status = response_status
        delivery.response_body = response_body[:1000]
        delivery.duration_ms = duration_ms

        if delivery.should_retry():
            delivery.status = WebhookDelivery.Status.RETRYING
            delays = [60, 300, 900]
            delay = delays[min(delivery.attempts - 1, len(delays) - 1)]
            delivery.next_retry_at = timezone.now() + timedelta(seconds=delay)
        else:
            delivery.status = WebhookDelivery.Status.FAILED

        delivery.save(
            update_fields=[
                "attempts",
                "response_status",
                "response_body",
                "duration_ms",
                "status",
                "next_retry_at",
            ]
        )
        cls._increment_webhook_stats(delivery.webhook, success=False)

    @staticmethod
    def _increment_webhook_stats(webhook: Webhook, *, success: bool) -> None:
        """Met a jour les compteurs de livraison du webhook (atomique via F())."""
        update_kwargs: dict[str, Any] = {
            "total_deliveries": models.F("total_deliveries") + 1,
            "last_delivery_at": timezone.now(),
        }
        if success:
            update_kwargs["successful_deliveries"] = models.F("successful_deliveries") + 1
        Webhook.objects.filter(pk=webhook.pk).update(**update_kwargs)

    @classmethod
    def send_delivery(cls, delivery: WebhookDelivery) -> bool:
        """Envoie une livraison de webhook.

        Args:
            delivery: Livraison a envoyer

        Returns:
            True si succes, False sinon
        """
        webhook = delivery.webhook
        payload_json = json.dumps(
            {
                "event": delivery.event_type,
                "timestamp": timezone.now().isoformat(),
                "data": delivery.payload,
            },
            default=str,
        )

        signature = webhook.generate_signature(payload_json)

        headers = {
            **cls.HEADERS,
            "X-Webhook-Signature": f"sha256={signature}",
            "X-Webhook-Event": delivery.event_type,
            "X-Webhook-Event-Id": str(delivery.event_id),
            "X-Webhook-Delivery-Id": str(delivery.pk),
        }

        start_time = time.perf_counter()

        try:
            response = requests.post(
                webhook.url,
                data=payload_json,
                headers=headers,
                timeout=cls.TIMEOUT,
            )
            duration_ms = int((time.perf_counter() - start_time) * 1000)

            if 200 <= response.status_code < 300:
                cls._mark_delivery_success(
                    delivery,
                    response.status_code,
                    response.text,
                    duration_ms,
                )
                logger.info(
                    "Webhook delivered: %s -> %s (status=%d, duration=%dms)",
                    delivery.event_type,
                    webhook.url,
                    response.status_code,
                    duration_ms,
                )
                return True
            cls._mark_delivery_failed(
                delivery,
                response.status_code,
                response.text,
                duration_ms,
            )
            logger.warning(
                "Webhook delivery failed: %s -> %s (status=%d)",
                delivery.event_type,
                webhook.url,
                response.status_code,
            )
            return False

        except requests.Timeout:
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            cls._mark_delivery_failed(
                delivery,
                None,
                "Timeout",
                duration_ms,
            )
            logger.warning(
                "Webhook timeout: %s -> %s",
                delivery.event_type,
                webhook.url,
            )
            return False

        except requests.RequestException as e:
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            cls._mark_delivery_failed(
                delivery,
                None,
                str(e),
                duration_ms,
            )
            logger.exception(
                "Webhook request error: %s -> %s",
                delivery.event_type,
                webhook.url,
            )
            return False

    @classmethod
    def toggle(cls, webhook: Webhook) -> bool:
        """Active/desactive un webhook.

        Args:
            webhook: Webhook a basculer

        Returns:
            Le nouvel etat is_active
        """
        webhook.is_active = not webhook.is_active
        webhook.save(update_fields=["is_active"])
        logger.info(
            "Webhook %s: %s (id=%d)",
            "active" if webhook.is_active else "desactive",
            webhook.name,
            webhook.pk,
        )
        return webhook.is_active

    @classmethod
    def retry_failed_deliveries(cls) -> int:
        """Retente les livraisons echouees.

        Returns:
            Nombre de livraisons retentees
        """
        now = timezone.now()
        deliveries = WebhookDelivery.objects.filter(
            status=WebhookDelivery.Status.RETRYING,
            next_retry_at__lte=now,
        ).select_related("webhook")

        count = 0
        for delivery in deliveries:
            if delivery.webhook.is_active:
                cls.send_delivery(delivery)
                count += 1

        return count
