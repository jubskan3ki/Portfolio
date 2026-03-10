"""Serializers pour les statuts de projets."""

from rest_framework import serializers

from ..models import ProjectStatus


class ProjectStatusSerializer(serializers.ModelSerializer[ProjectStatus]):
    """Serializer pour les statuts de projets."""

    class Meta:
        model = ProjectStatus
        fields = ("id", "name", "description")
        read_only_fields = ("id",)
