"""
Sérialisation des messages de contact.
"""

import re

from rest_framework import serializers

from ..models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Sérialisation enrichie avec validation avancée des messages de contact.
    """

    subject_display = serializers.CharField(source="get_subject_display", read_only=True)
    short_message = serializers.SerializerMethodField()

    class Meta:
        """
        Métadonnées de la sérialisation.
        """

        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "subject",
            "subject_display",
            "message",
            "short_message",
            "is_read",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_read",
            "created_at",
            "updated_at",
            "subject_display",
            "short_message",
        ]

    def get_short_message(self, obj):
        """Renvoie un extrait court du message."""
        message = obj.message.strip()
        return f"{message[:47]}..." if len(message) > 50 else message

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

    def validate_phone_number(self, value):
        """Validation stricte du numéro de téléphone (format international)."""
        if value:
            cleaned_number = re.sub(r"\s+", "", value)
            if not re.match(r"^\+?1?\d{8,15}$", cleaned_number):
                raise serializers.ValidationError("Numéro de téléphone invalide (format international requis).")
            return cleaned_number
        return value

    def validate_subject(self, value):
        """Validation stricte du sujet (choix limité)."""
        if value not in dict(ContactMessage.SUBJECT_CHOICES).keys():
            raise serializers.ValidationError("Sujet non valide.")
        return value
