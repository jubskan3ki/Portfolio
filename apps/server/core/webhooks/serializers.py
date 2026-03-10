"""Serializers pour le module webhooks."""

from rest_framework import serializers

from .models import Webhook, WebhookDelivery, WebhookEventType


class WebhookSerializer(serializers.ModelSerializer):
    """Serializer pour les webhooks."""

    events = serializers.MultipleChoiceField(
        choices=WebhookEventType.choices,
        help_text="Liste des evenements a surveiller",
    )
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Webhook
        fields = [
            "id",
            "name",
            "url",
            "events",
            "is_active",
            "total_deliveries",
            "successful_deliveries",
            "success_rate",
            "last_delivery_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "total_deliveries",
            "successful_deliveries",
            "last_delivery_at",
            "created_at",
            "updated_at",
        ]

    def get_success_rate(self, obj: Webhook) -> float:
        """Calcule le taux de succes."""
        if obj.total_deliveries == 0:
            return 100.0
        return round((obj.successful_deliveries / obj.total_deliveries) * 100, 2)

    def create(self, validated_data: dict) -> Webhook:
        """Cree un webhook avec l'utilisateur courant."""
        validated_data["created_by"] = self.context["request"].user
        validated_data["events"] = list(validated_data["events"])
        return super().create(validated_data)

    def update(self, instance: Webhook, validated_data: dict) -> Webhook:
        """Met a jour un webhook."""
        if "events" in validated_data:
            validated_data["events"] = list(validated_data["events"])
        return super().update(instance, validated_data)


class WebhookCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la creation de webhooks."""

    events = serializers.MultipleChoiceField(
        choices=WebhookEventType.choices,
        help_text="Liste des evenements a surveiller",
    )

    class Meta:
        model = Webhook
        fields = ["name", "url", "events", "is_active"]


class WebhookDeliverySerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des livraisons."""

    webhook_name = serializers.CharField(source="webhook.name", read_only=True)
    event_type_display = serializers.CharField(
        source="get_event_type_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = WebhookDelivery
        fields = [
            "id",
            "webhook",
            "webhook_name",
            "event_type",
            "event_type_display",
            "payload",
            "status",
            "status_display",
            "response_status",
            "attempts",
            "next_retry_at",
            "created_at",
            "delivered_at",
            "duration_ms",
        ]
        read_only_fields = fields


class WebhookEventTypesSerializer(serializers.Serializer):
    """Serializer pour lister les types d'evenements disponibles."""

    value = serializers.CharField()
    event_label = serializers.CharField()

    def to_representation(self, instance: dict) -> dict:
        """Renomme event_label en label pour la sortie."""
        return {
            "value": instance["value"],
            "label": instance["label"],
        }
