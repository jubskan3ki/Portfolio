"""
Sérialisation complète et sécurisée pour la réinitialisation du mot de passe de l'administrateur.
"""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from ..models import ResetPasswordCode, User


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
    Sérialisation avancée pour valider le code, vérifier la sécurité du mot de passe et effectuer la réinitialisation.
    """

    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        """
        Vérifie que le mot de passe est sécurisé.
        """
        validate_password(value)
        return value

    def validate(self, attrs):
        """
        Vérifie que le code est correct et non expiré.
        """
        reset_code = get_object_or_404(ResetPasswordCode, email=attrs["email"], code=attrs["code"])

        if reset_code.is_expired():
            raise serializers.ValidationError("Le code est expiré.")

        user = get_object_or_404(User, email=attrs["email"])
        if user.check_password(attrs["new_password"]):
            raise serializers.ValidationError("Le nouveau mot de passe doit être différent de l'ancien.")

        return attrs

    def save(self, **kwargs):
        """
        Met à jour le mot de passe et supprime le code utilisé.
        """
        user = get_object_or_404(User, email=self.validated_data["email"])
        user.password = make_password(self.validated_data["new_password"])
        user.last_password_change = timezone.now()
        user.save()

        ResetPasswordCode.objects.filter(email=self.validated_data["email"]).delete()

    def create(self, validated_data):
        raise NotImplementedError("Cette action n'est pas autorisée.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Cette action n'est pas autorisée.")
