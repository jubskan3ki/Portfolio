"""
Sérialisation des messages de contact.
"""

import re

from rest_framework import serializers

from ..models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Sérialisation des messages de contact avec validation stricte.
    """

    class Meta:
        """
        Métadonnées de la sérialisation.
        """

        model = ContactMessage
        fields = ["id", "name", "email", "message", "created_at"]

    def validate_name(self, value):
        """Le nom doit contenir au moins 2 caractères et pas de caractères spéciaux interdits."""
        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        if not re.match(r"^[A-Za-zÀ-ÿ '-]+$", cleaned_value):
            raise serializers.ValidationError("Le nom contient des caractères non autorisés.")
        return cleaned_value

    def validate_email(self, value):
        """Validation stricte de l'email (basique ici, DNS check en option)."""
        cleaned_email = value.strip().lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", cleaned_email):
            raise serializers.ValidationError("Adresse email invalide.")
        return cleaned_email

    def validate_message(self, value):
        """Le message doit contenir au moins 10 caractères et limiter les répétitions."""
        cleaned_message = value.strip()
        if len(cleaned_message) < 10:
            raise serializers.ValidationError("Le message doit contenir au moins 10 caractères.")
        if cleaned_message.lower().count("http") > 3:
            raise serializers.ValidationError("Trop de liens dans le message.")
        return cleaned_message
