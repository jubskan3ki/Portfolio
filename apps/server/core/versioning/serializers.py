"""Serializers pour le module versioning."""

from rest_framework import serializers

from .models import Version


class VersionSerializer(serializers.ModelSerializer):
    """Serialisation d'une Version (snapshot lisible)."""

    created_by_email = serializers.CharField(source="created_by.email", default=None, read_only=True)

    class Meta:
        model = Version
        fields = [
            "id",
            "content_type",
            "object_id",
            "version_number",
            "snapshot",
            "created_at",
            "created_by_email",
        ]
        read_only_fields = fields
