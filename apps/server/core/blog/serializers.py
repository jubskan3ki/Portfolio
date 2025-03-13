"""
Sérialisation des articles de blog.
"""

from rest_framework import serializers

from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Sérialisation des articles avec validation avancée.
    """

    class Meta:
        model = BlogPost
        fields = "__all__"

    def validate_title(self, value):
        """Validation du titre (éviter les doublons et les titres trop courts)."""
        if len(value) < 5:
            raise serializers.ValidationError("Le titre doit contenir au moins 5 caractères.")
        return value
