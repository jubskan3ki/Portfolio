"""Serializers pour la gestion des mots de passe."""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from utils.serializers.base import ReadOnlySerializer
from utils.validators import (
    EMAIL_REGEX,
    RESET_CODE_REGEX,
)
from utils.validators import validate_password as validate_password_strength


class RequestResetPasswordSerializer(ReadOnlySerializer):
    """Serializer pour la demande de reinitialisation de mot de passe."""

    email = serializers.EmailField(required=True)

    def validate_email(self, value: str) -> str:
        """Verifie le format de l'email."""
        if not EMAIL_REGEX.match(value):
            raise serializers.ValidationError("Format d'email invalide.")
        return value


class ResetPasswordSerializer(ReadOnlySerializer):
    """Serializer pour la reinitialisation effective du mot de passe."""

    email = serializers.EmailField(required=True)
    reset_code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_reset_code(self, value: str) -> str:
        """Valide le format du code de reinitialisation."""
        if not RESET_CODE_REGEX.match(value):
            raise serializers.ValidationError(
                "Le code doit contenir 8 caracteres alphanumeriques (majuscules et chiffres)."
            )
        return value

    def validate_new_password(self, value: str) -> str:
        """Valide la securite du mot de passe."""
        try:
            validate_password_strength(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages) from e
        return value


class ChangePasswordSerializer(ReadOnlySerializer):
    """Serializer pour le changement de mot de passe (utilisateur connecte)."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value: str) -> str:
        """Valide la securite du nouveau mot de passe."""
        try:
            validate_password_strength(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages) from e
        return value
