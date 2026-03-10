"""Serializers pour l'administration."""

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.serializers.base import ReadOnlySerializer

user_model = get_user_model()


class AdminLoginSerializer(ReadOnlySerializer):
    """Serializer pour la connexion admin."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)


class AdminProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil administrateur (lecture seule)."""

    class Meta:
        """Configuration du serializer."""

        model = user_model
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_active",
            "bio",
            "avatar",
            "position",
            "public_email",
            "linkedin",
            "github",
            "twitter",
            "date_joined",
            "updated_at",
        ]
        read_only_fields = fields


class AdminUpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer pour la mise a jour du profil administrateur."""

    class Meta:
        """Configuration du serializer."""

        model = user_model
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "bio",
            "avatar",
            "position",
            "public_email",
            "linkedin",
            "github",
            "twitter",
        ]

    def validate_avatar(self, value):
        """Valide la taille et le format de l'avatar."""
        if not value:
            return value

        if value.size > settings.MAX_AVATAR_SIZE:
            raise serializers.ValidationError("L'image ne doit pas depasser 5MB.")

        ext = value.name.split(".")[-1].lower()
        if ext not in settings.ALLOWED_AVATAR_EXTENSIONS:
            raise serializers.ValidationError(
                f"Format non supporte. Formats acceptes: {', '.join(settings.ALLOWED_AVATAR_EXTENSIONS)}"
            )

        return value


class AdminRefreshSerializer(ReadOnlySerializer):
    """Serializer pour le rafraichissement des tokens JWT."""

    refresh = serializers.CharField(required=True, help_text="Token de rafraichissement JWT")

    def validate_refresh(self, value):
        """Valide le format du token."""
        if not value or not isinstance(value, str):
            raise serializers.ValidationError("Le token doit etre une chaine non vide.")

        parts = value.split(".")
        if len(parts) != 3:
            raise serializers.ValidationError("Format de token JWT invalide.")

        return value
