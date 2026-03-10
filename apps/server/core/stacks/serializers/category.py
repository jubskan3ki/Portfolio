"""Serializer pour les categories de stacks."""

from rest_framework import serializers

from ..models import StackCategory


class StackCategorySerializer(serializers.ModelSerializer):
    """Serializer pour les categories de stacks."""

    count = serializers.SerializerMethodField()

    class Meta:
        model = StackCategory
        fields = ("id", "name", "description", "icon", "count")
        read_only_fields = ("id", "count")

    def get_count(self, obj: StackCategory) -> int:
        """Retourne le nombre de stacks.

        Uses 'stacks_count' annotation when available (list/retrieve).
        Falls back to 0 for single-object responses (create/update)
        where annotation is not present.
        """
        stacks_count = getattr(obj, "stacks_count", None)
        if stacks_count is not None:
            return int(stacks_count)
        return 0
