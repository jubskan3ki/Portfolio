"""
Sérialisation enrichie et optimisée des données de l'administrateur unique.
"""

from rest_framework import serializers

from ..models import User


class AdminSerializer(serializers.ModelSerializer):
    """
    Sérialisation complète des informations de l'admin (lecture seule).
    """

    class Meta:
        """
        Métadonnées de la classe.
        """

        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "bio",
            "avatar",
            "date_joined",
            "last_password_change",
        ]


class UpdateAdminSerializer(serializers.ModelSerializer):
    """
    Mise à jour complète des informations de l'admin.
    """

    class Meta:
        """
        Métadonnées de la classe.
        """

        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "bio", "avatar"]
