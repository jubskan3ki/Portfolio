"""
Sérialisation des technologies et stacks.
"""

from django.utils.text import slugify
from rest_framework import serializers

from ..models import Stack


class StackSerializer(serializers.ModelSerializer):
    """
    Sérialisation enrichie des stacks technologiques.
    """

    proficiency_label = serializers.CharField(source="get_proficiency_display", read_only=True)

    class Meta:
        """
        Métadonnées enrichies du serializer Stack.
        """

        model = Stack
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "category",
            "proficiency",
            "proficiency_label",
            "description",
            "official_website",
            "experience_years",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at", "proficiency_label"]

    def validate_proficiency(self, value):
        """Vérifie que la proficiency est entre 1 et 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Le niveau de maîtrise doit être entre 1 et 5.")
        return value

    def validate_experience_years(self, value):
        """Vérifie que le nombre d'années d'expérience est réaliste."""
        if value < 0 or value > 50:
            raise serializers.ValidationError("Le nombre d'années d'expérience doit être compris entre 0 et 50.")
        return value

    def validate_icon(self, value):
        """Validation sur la taille de l'icône (max 2MB)."""
        max_size = 2 * 1024 * 1024  # 2MB
        if value and value.size > max_size:
            raise serializers.ValidationError("L'icône ne doit pas dépasser 2MB.")
        return value

    def create(self, validated_data):
        """Génération automatique du slug lors de la création."""
        validated_data["slug"] = validated_data.get("slug") or slugify(validated_data["name"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Mise à jour automatique du slug si le nom change."""
        if "name" in validated_data and instance.name != validated_data["name"]:
            validated_data["slug"] = slugify(validated_data["name"])
        return super().update(instance, validated_data)
