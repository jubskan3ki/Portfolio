"""Serialiseurs pour les tags d'articles."""

from rest_framework import serializers

from ..models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serialiseur pour les tags d'articles."""

    count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "count"]
        read_only_fields = ["id", "count"]

    def get_count(self, obj: Tag) -> int:
        """Retourne le nombre d'articles (utilise la propriete du modele)."""
        return obj.article_count
