"""Serializer pour les ressources de stacks."""

from rest_framework import serializers

from ..models import RESOURCE_TYPES, StackResource


class StackResourceSerializer(serializers.ModelSerializer):
    """Serializer pour les ressources liees aux stacks."""

    type_display = serializers.SerializerMethodField()

    class Meta:
        model = StackResource
        fields = ("id", "stack", "title", "description", "url", "type", "type_display", "is_featured")
        read_only_fields = ("id", "type_display")

    def get_type_display(self, obj: StackResource) -> str:
        """Retourne le label lisible du type."""
        return dict(RESOURCE_TYPES).get(obj.type, obj.type)
