"""
Sérialisation des données de l'administrateur unique.
"""

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import ResetPasswordCode, User


class AdminSerializer(serializers.ModelSerializer):
    """
    Sérialisation des informations de l'admin (lecture seule).
    """

    class Meta:
        model = User
        fields = ["email"]


class UpdateAdminSerializer(serializers.ModelSerializer):
    """
    Mise à jour des informations de l'admin.
    """

    class Meta:
        model = User
        fields = ["email"]


class RequestResetPasswordSerializer(serializers.Serializer):
    """
    Sérialisation pour demander un code de réinitialisation.
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Vérifie que l'email correspond à l'admin.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun administrateur trouvé avec cet email.")
        return value

    def create(self, validated_data):
        """
        Création non autorisée.
        """
        raise NotImplementedError("Cette action n'est pas autorisée.")

    def update(self, instance, validated_data):
        """
        Mise à jour non applicable.
        """
        raise NotImplementedError("Cette action n'est pas autorisée.")


class ResetPasswordSerializer(serializers.Serializer):
    """
    Sérialisation pour valider le code et changer le mot de passe en une seule étape.
    """

    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Vérifie que le code est correct et non expiré.
        """
        reset_code = get_object_or_404(ResetPasswordCode, email=attrs["email"], code=attrs["code"])

        if reset_code.is_expired():
            raise serializers.ValidationError("Le code est expiré.")

        admin = get_object_or_404(User, email=attrs["email"])
        if admin.check_password(attrs["new_password"]):
            raise serializers.ValidationError("Le nouveau mot de passe doit être différent de l'ancien.")

        return attrs

    def save(self, **kwargs):
        """
        Met à jour le mot de passe et supprime le code utilisé.
        """
        admin = get_object_or_404(User, email=self.validated_data["email"])
        admin.password = make_password(self.validated_data["new_password"])
        admin.save()

        ResetPasswordCode.objects.filter(email=self.validated_data["email"]).delete()

    def create(self, validated_data):
        raise NotImplementedError("Cette action n'est pas autorisée.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Cette action n'est pas autorisée.")
