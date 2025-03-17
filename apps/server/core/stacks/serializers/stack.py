"""
Sérialisation des technologies et stacks.
"""

from rest_framework import serializers

from ..models import Stack


class StackSerializer(serializers.ModelSerializer):
    """
    Sérialisation des stacks technologiques.
    """

    class Meta:
        """
        Métadonnées de la sérialisation.
        """

        model = Stack
        fields = ["id", "name", "icon", "category", "proficiency", "created_at", "updated_at"]

    def validate_proficiency(self, value):
        """S'assure que la proficiency est entre 1 et 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Le niveau de maîtrise doit être entre 1 et 5.")
        return value
