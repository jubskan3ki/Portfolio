"""Serializers pour les types d'experiences."""

from rest_framework import serializers

from ..models import ExperienceType


class ExperienceTypeSerializer(serializers.ModelSerializer):
    """Serializer pour les types d'experiences."""

    class Meta:
        model = ExperienceType
        fields = ["id", "name", "icon"]
        read_only_fields = ["id"]
