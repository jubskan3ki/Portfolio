"""
Sérialisation des projets du portfolio.
"""

from rest_framework import serializers

from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialisation des projets avec validation avancée.
    """

    class Meta:
        """
        Métadonnées de la sérialisation.
        """

        model = Project
        fields = ["id", "title", "description", "image", "github_link", "live_demo", "tags", "created_at", "updated_at"]

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
