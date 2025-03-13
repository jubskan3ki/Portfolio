"""
Sérialisation des projets du portfolio.
"""

from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialisation des projets avec validation avancée.
    """

    class Meta:
        model = Project
        fields = "__all__"

    def validate_github_link(self, value):
        """Validation de l'URL GitHub."""
        if value and not value.startswith("https://github.com/"):
            raise serializers.ValidationError("L'URL GitHub doit commencer par 'https://github.com/'")
        return value

    def validate_live_demo(self, value):
        """Validation de l'URL Live Demo."""
        if value and not value.startswith("https://"):
            raise serializers.ValidationError("L'URL du live demo doit être en HTTPS.")
        return value
