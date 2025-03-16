"""
Sérialisation des données de l'administrateur unique.
"""

from rest_framework import serializers

from ..models import User


class AdminSerializer(serializers.ModelSerializer):
    """
    Sérialisation des informations de l'admin (lecture seule).
    """

    class Meta:
        """
        Métadonnées de la classe.
        """

        model = User
        fields = ["email"]


class UpdateAdminSerializer(serializers.ModelSerializer):
    """
    Mise à jour des informations de l'admin.
    """

    class Meta:
        """
        Métadonnées de la classe.
        """

        model = User
        fields = ["email"]
