"""Serialiseurs pour les tags d'articles."""

from rest_framework import serializers

from ..models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serialiseur pour les tags d'articles."""

    count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "count", "view_count"]
        read_only_fields = ["id", "count", "view_count"]

    def get_count(self, obj: Tag) -> int:
        """Retourne le nombre d'articles (utilise la propriete du modele)."""
        return obj.article_count

    def get_view_count(self, obj: Tag) -> int:
        """Retourne la somme des vues des articles publies lies."""
        return obj.total_view_count
