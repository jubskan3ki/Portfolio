"""
Sérialisation des technologies et stacks.
"""

from rest_framework import serializers

from .models import Stack


class StackSerializer(serializers.ModelSerializer):
    """
    Sérialisation des stacks technologiques.
    """

    class Meta:
        model = Stack
        fields = "__all__"

    def validate_proficiency(self, value):
        """Validation du niveau de maîtrise (doit être entre 1 et 5)."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Le niveau de maîtrise doit être entre 1 et 5.")
        return value
