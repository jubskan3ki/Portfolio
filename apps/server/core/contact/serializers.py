"""
Sérialisation des messages de contact.
"""

from rest_framework import serializers

from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Sérialisation des messages de contact avec validation stricte.
    """

    class Meta:
        model = ContactMessage
        fields = "__all__"

    def validate_message(self, value):
        """
        Vérifie que le message contient au moins 10 caractères.
        """
        if len(value) < 10:
            raise serializers.ValidationError("Le message doit contenir au moins 10 caractères.")
        return value
