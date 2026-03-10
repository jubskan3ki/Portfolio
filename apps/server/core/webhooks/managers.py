"""Managers pour le module webhooks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from core.webhooks.models import Webhook, WebhookDelivery


class WebhookManager(models.Manager["Webhook"]):
    """Manager pour les webhooks."""

    def get_queryset(self) -> models.QuerySet[Webhook]:
        return super().get_queryset().select_related("created_by")

    def active(self) -> models.QuerySet[Webhook]:
        """Webhooks actifs."""
        return self.get_queryset().filter(is_active=True)

    def for_event(self, event_type: str) -> models.QuerySet[Webhook]:
        """Webhooks abonnes a un type d'evenement."""
        return self.active().filter(models.Q(events__contains=[event_type]) | models.Q(events__contains=["*"]))


class WebhookDeliveryManager(models.Manager["WebhookDelivery"]):
    """Manager pour les livraisons de webhooks."""

    def get_queryset(self) -> models.QuerySet[WebhookDelivery]:
        return super().get_queryset().select_related("webhook")

    def pending_retries(self) -> models.QuerySet[WebhookDelivery]:
        """Livraisons en attente de nouvelle tentative."""
        from django.utils import timezone

        return self.get_queryset().filter(
            status="retrying",
            next_retry_at__lte=timezone.now(),
        )
