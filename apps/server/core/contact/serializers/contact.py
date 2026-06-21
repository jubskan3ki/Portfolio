"""Serialiseurs pour les soumissions de formulaire de contact."""

from rest_framework import serializers

from utils.serializers.base import ReadOnlySerializer

from ..models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """Serialiseur pour la soumission de formulaire de contact.

    Note: pas de separation List/Detail/Write car Contact est un endpoint
    write-heavy (soumission formulaire). Le meme serializer sert pour
    la creation (public) et la lecture (admin).
    """

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "phone",
            "company",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "message": {"max_length": 5000},
        }

    def validate_email(self, value):
        """Normalise l'email (DRF EmailField valide deja le format)."""
        return value.lower().strip()

    def validate_name(self, value):
        """Valide que le nom n'est pas vide apres nettoyage."""
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Le nom ne peut pas etre vide.")
        if len(cleaned) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caracteres.")
        return cleaned

    def validate_message(self, value):
        """Valide que le message a une longueur minimale."""
        cleaned = value.strip()
        if len(cleaned) < 10:
            raise serializers.ValidationError("Le message doit contenir au moins 10 caracteres.")
        return cleaned


class ContactAdminWriteSerializer(serializers.ModelSerializer):
    """Serialiseur d'edition admin d'une soumission de contact.

    Expose uniquement les champs reellement modifiables par l'admin
    (statut + reponse). Le serializer public de creation (ContactSerializer)
    ne doit pas exposer ces champs.
    """

    class Meta:
        model = Contact
        fields = [
            "status",
            "response_message",
            "response_date",
        ]

    def validate_status(self, value):
        """Valide que le statut fait partie des valeurs autorisees."""
        allowed = {choice[0] for choice in Contact.STATUS_CHOICES}
        if value not in allowed:
            raise serializers.ValidationError(f"Statut invalide. Valeurs autorisees : {', '.join(sorted(allowed))}.")
        return value


class ContactResponseSerializer(ReadOnlySerializer):
    """Serialiseur pour la reponse de soumission du formulaire."""

    success = serializers.BooleanField()
    message = serializers.CharField()
    error_details = serializers.DictField(required=False, allow_empty=True)
    referenceId = serializers.CharField(required=False, allow_blank=True)
