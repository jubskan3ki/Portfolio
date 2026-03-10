"""Serializers pour le module audit."""

from rest_framework import serializers

from .models import AuditLog


class AuditLogListSerializer(serializers.ModelSerializer):
    """Serializer leger pour la liste des logs d'audit."""

    user_email = serializers.CharField(source="user.email", default=None, read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "action",
            "model_name",
            "object_id",
            "object_repr",
            "user_email",
            "ip_address",
            "timestamp",
        ]
        read_only_fields = fields


class AuditLogDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour le detail d'un log d'audit."""

    user_email = serializers.CharField(source="user.email", default=None, read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "action",
            "model_name",
            "object_id",
            "object_repr",
            "changes",
            "user_email",
            "ip_address",
            "user_agent",
            "correlation_id",
            "timestamp",
        ]
        read_only_fields = fields
