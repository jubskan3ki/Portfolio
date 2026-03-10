"""Serializers pour la pagination."""

from typing import Any

from rest_framework import serializers


class PaginationMetaSerializer(serializers.Serializer):
    """Serializer pour les metadonnees de pagination."""

    total = serializers.IntegerField(help_text="Nombre total d'elements")
    page = serializers.IntegerField(help_text="Page actuelle")
    limit = serializers.IntegerField(help_text="Elements par page")
    total_pages = serializers.IntegerField(
        help_text="Nombre total de pages",
        source="totalPages",
    )


class PaginatedResponseSerializer[T](serializers.Serializer):
    """Serializer generique pour les reponses paginee.

    Usage:
        class ArticlePaginatedSerializer(PaginatedResponseSerializer):
            data = ArticleListSerializer(many=True)
    """

    pagination = PaginationMetaSerializer()

    def __init__(self, *args: Any, data_serializer: type[serializers.Serializer] | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if data_serializer:
            self.fields["data"] = data_serializer(many=True)


class SimplePaginatedSerializer(serializers.Serializer):
    """Serializer simplifie pour les listes paginee.

    Utilise quand la structure de pagination est simple.
    """

    count = serializers.IntegerField(help_text="Nombre total d'elements")
    next = serializers.URLField(
        allow_null=True,
        help_text="URL de la page suivante",
    )
    previous = serializers.URLField(
        allow_null=True,
        help_text="URL de la page precedente",
    )
    results = serializers.ListField(help_text="Liste des resultats")
