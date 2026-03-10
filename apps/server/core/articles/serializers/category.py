"""Serialiseurs pour les categories d'articles."""

from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serialiseur pour les categories d'articles."""

    count = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "count"]
        read_only_fields = ["id", "slug", "count"]

    def get_count(self, obj: Category) -> int:
        """Retourne le nombre d'articles (utilise la propriete du modele)."""
        return obj.article_count
