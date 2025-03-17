"""
Sérialisation des articles de blog.
"""

from rest_framework import serializers

from ..models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Sérialisation des articles avec validation avancée.
    """

    class Meta:
        """
        Métadonnées du sérialiseur.
        """

        model = BlogPost
        fields = ["id", "title", "content", "image", "category", "tags", "created_at", "updated_at"]

    def validate_title(self, value):
        """
        Validation du titre (longueur minimale).
        """
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Le titre doit contenir au moins 5 caractères.")
        return value

    def validate_image(self, value):
        """
        Limitation de la taille de l'image (2 Mo max).
        """
        max_size = 2 * 1024 * 1024
        if value and value.size > max_size:
            raise serializers.ValidationError("L'image ne doit pas dépasser 2 Mo.")
        return value
