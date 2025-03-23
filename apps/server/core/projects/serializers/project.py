"""
Sérialisation des projets du portfolio.
"""

from django.utils.text import slugify
from rest_framework import serializers

from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialisation complète des projets avec validations avancées.
    """

    is_active = serializers.ReadOnlyField()
    duration = serializers.ReadOnlyField()
    priority_label = serializers.ReadOnlyField(source="get_priority_display")

    class Meta:
        """
        Métadonnées de la sérialisation.
        """

        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "image",
            "github_link",
            "live_demo",
            "tags",
            "status",
            "priority",
            "priority_label",
            "start_date",
            "end_date",
            "duration",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def validate_github_link(self, value):
        """Validation stricte de l'URL GitHub."""
        if value and not value.startswith("https://github.com/"):
            raise serializers.ValidationError("L'URL GitHub doit commencer par 'https://github.com/'.")
        return value

    def validate_live_demo(self, value):
        """Validation stricte pour un lien HTTPS uniquement."""
        if value and not value.startswith("https://"):
            raise serializers.ValidationError("L'URL du live demo doit être en HTTPS.")
        return value

    def validate_image(self, value):
        """Validation optionnelle sur le poids de l'image."""
        max_size = 2 * 1024 * 1024
        if value and value.size > max_size:
            raise serializers.ValidationError("L'image ne doit pas dépasser 2MB.")
        return value

    def validate_priority(self, value):
        """Validation stricte de la priorité."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError("La priorité doit être comprise entre 1 et 10.")
        return value

    def validate_tags(self, value):
        """Validation stricte des tags sous forme de liste."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Les tags doivent être fournis sous forme de liste.")
        return value

    def validate(self, attrs):
        """Validation stricte des dates de début et de fin."""
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("La date de début doit être antérieure à la date de fin.")
        return attrs

    def create(self, validated_data):
        """Création d'un projet avec slug automatique."""
        validated_data.setdefault("slug", slugify(validated_data["title"]))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Mise à jour d'un projet avec slug automatique."""
        if "title" in validated_data:
            validated_data["slug"] = slugify(validated_data["title"])
        return super().update(instance, validated_data)
