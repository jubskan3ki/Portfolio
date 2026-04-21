"""Admin pour le module webhooks."""

from typing import ClassVar

from django.contrib import admin

from .models import Webhook, WebhookDelivery


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    """Admin pour les webhooks."""

    list_display = [
        "name",
        "url",
        "is_active",
        "total_deliveries",
        "successful_deliveries",
        "success_rate",
        "last_delivery_at",
        "created_by",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "url"]
    readonly_fields = [
        "secret",
        "total_deliveries",
        "successful_deliveries",
        "last_delivery_at",
        "created_at",
        "updated_at",
    ]
    filter_horizontal: ClassVar[list[str]] = []

    @admin.display(description="Taux de succes")
    def success_rate(self, obj: Webhook) -> str:
        """Affiche le taux de succes."""
        if obj.total_deliveries == 0:
            return "N/A"
        rate = (obj.successful_deliveries / obj.total_deliveries) * 100
        return f"{rate:.1f}%"


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    """Admin pour les livraisons de webhooks."""

    list_display = [
        "id",
        "webhook",
        "event_type",
        "status",
        "response_status",
        "attempts",
        "duration_ms",
        "created_at",
    ]
    list_filter = ["status", "event_type", "created_at"]
    search_fields = ["webhook__name", "webhook__url"]
    readonly_fields = [
        "webhook",
        "event_type",
        "payload",
        "status",
        "response_status",
        "response_body",
        "attempts",
        "next_retry_at",
        "created_at",
        "delivered_at",
        "duration_ms",
    ]
    list_select_related = ["webhook"]

    def has_add_permission(self, _request) -> bool:
        """Interdit la creation manuelle."""
        return False

    def has_change_permission(self, _request, _obj=None) -> bool:
        """Interdit la modification."""
        return False
