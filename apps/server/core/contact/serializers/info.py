"""Serialiseurs pour les informations de contact."""

from typing import Any

from rest_framework import serializers

from ..models import ContactInfo
from ..services import ContactInfoService


class ContactInfoSerializer(serializers.ModelSerializer):
    """Serialiseur pour les informations de contact."""

    address = serializers.SerializerMethodField()
    socialMedia = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = ContactInfo
        fields = ["id", "email", "phone", "bio", "address", "socialMedia", "availability"]

    def get_address(self, obj: ContactInfo) -> dict[str, str | None] | None:
        """Construit l'objet d'adresse."""
        if not (obj.street or obj.city or obj.zip_code or obj.country):
            return None

        return {
            "street": obj.street or None,
            "city": obj.city or None,
            "zipCode": obj.zip_code or None,
            "country": obj.country or None,
        }

    def get_socialMedia(self, obj: ContactInfo) -> dict[str, str | None] | None:
        """Construit l'objet de medias sociaux."""
        if not (obj.linkedin or obj.github or obj.twitter or obj.medium):
            return None

        return {
            "linkedin": obj.linkedin or None,
            "github": obj.github or None,
            "twitter": obj.twitter or None,
            "medium": obj.medium or None,
        }

    def get_availability(self, obj: ContactInfo) -> dict[str, Any]:
        """Construit l'objet de disponibilite."""
        return {
            "status": obj.availability_status,
            "message": obj.availability_message or None,
        }

    def get_bio(self, _obj: ContactInfo) -> str | None:
        """Recupere la bio de l'utilisateur admin (proprietaire du portfolio)."""
        return ContactInfoService.get_admin_bio()
