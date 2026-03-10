"""Serializers de base reutilisables."""

from typing import Any

from rest_framework import serializers


class WriteOnlyModelSerializer(serializers.ModelSerializer):
    """Serializer pour les operations d'ecriture (create/update).

    Configure pour valider les donnees entrantes.
    """

    class Meta:
        abstract = True


class ReadOnlySerializer(serializers.Serializer):
    """Serializer en lecture seule (non-ModelSerializer).

    Elimine le boilerplate create/update → NotImplementedError
    pour les serializers de pagination, timeline, stats, etc.
    """

    def create(self, validated_data: Any) -> Any:
        raise NotImplementedError("Serializer en lecture seule")

    def update(self, instance: Any, validated_data: Any) -> Any:
        raise NotImplementedError("Serializer en lecture seule")


class SlugLookupMixin:
    """Mixin pour les serializers qui utilisent un slug comme lookup field.

    Ajoute la validation du slug et des methodes utilitaires.
    """

    slug = serializers.SlugField(
        max_length=255,
        help_text="Identifiant unique pour l'URL",
    )

    def validate_slug(self, value: str) -> str:
        """Valide et normalise le slug."""
        return value.lower().strip()
