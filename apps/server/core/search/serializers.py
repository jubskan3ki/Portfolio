"""Serializers pour l'endpoint /api/search/."""

from rest_framework import serializers

from .services import MIN_QUERY_LENGTH, VALID_TYPES


class SearchQuerySerializer(serializers.Serializer):
    """Validation des parametres de la requete de recherche."""

    q = serializers.CharField(required=True, min_length=MIN_QUERY_LENGTH, max_length=200)
    type = serializers.ChoiceField(choices=VALID_TYPES, default="all")
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=50, default=10)


class SearchResultSerializer(serializers.Serializer):
    """Un resultat unitaire, discriminateur 'type'."""

    type = serializers.CharField(help_text="article | project | stack | experience")
    id = serializers.IntegerField()
    slug = serializers.CharField(allow_blank=True)
    title = serializers.CharField()
    url = serializers.CharField()
    rank = serializers.FloatField()
    snippet = serializers.CharField(allow_blank=True, help_text="Extrait surligne via <mark>.")
    metadata = serializers.DictField()
