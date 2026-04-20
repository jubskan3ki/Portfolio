"""Serialiseurs pour les informations de contact."""

from typing import Any

from rest_framework import serializers

from ..models import ContactInfo
from ..services import ContactInfoService


class ContactInfoSerializer(serializers.ModelSerializer):
    """Serialiseur pour les informations de contact.

    - Lecture : champs imbriques (address, socialMedia, availability) + bio
    - Ecriture : champs plats du modele OU cles imbriquees (converties via to_internal_value)
    """

    address = serializers.SerializerMethodField()
    socialMedia = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = ContactInfo
        fields = [
            "id",
            "email",
            "phone",
            "bio",
            "address",
            "socialMedia",
            "availability",
            # Champs plats writable (caches en lecture par les SerializerMethodField)
            "street",
            "city",
            "zip_code",
            "country",
            "linkedin",
            "github",
            "twitter",
            "medium",
            "availability_status",
            "availability_message",
            "is_primary",
        ]
        extra_kwargs = {
            "street": {"write_only": True, "required": False, "allow_blank": True},
            "city": {"write_only": True, "required": False, "allow_blank": True},
            "zip_code": {"write_only": True, "required": False, "allow_blank": True},
            "country": {"write_only": True, "required": False, "allow_blank": True},
            "linkedin": {"write_only": True, "required": False, "allow_blank": True},
            "github": {"write_only": True, "required": False, "allow_blank": True},
            "twitter": {"write_only": True, "required": False, "allow_blank": True},
            "medium": {"write_only": True, "required": False, "allow_blank": True},
            "availability_status": {"write_only": True, "required": False},
            "availability_message": {"write_only": True, "required": False, "allow_blank": True},
        }

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
        """Construit l'objet de disponibilite avec un libelle par defaut selon le statut."""
        default_messages = {
            "available": "Disponible pour de nouveaux projets",
            "limited": "Disponibilite limitee",
            "unavailable": "Indisponible actuellement",
        }
        message = obj.availability_message or default_messages.get(obj.availability_status, "")
        return {
            "status": obj.availability_status,
            "message": message,
        }

    def get_bio(self, _obj: ContactInfo) -> str | None:
        """Recupere la bio de l'utilisateur admin (proprietaire du portfolio)."""
        return ContactInfoService.get_admin_bio()

    def to_internal_value(self, data: Any) -> dict[str, Any]:
        """Accepte aussi les cles imbriquees (address, socialMedia, availability) a l'ecriture."""
        if isinstance(data, dict):
            data = dict(data)
            address = data.pop("address", None)
            if isinstance(address, dict):
                if "street" in address:
                    data["street"] = address.get("street") or ""
                if "city" in address:
                    data["city"] = address.get("city") or ""
                if "zipCode" in address:
                    data["zip_code"] = address.get("zipCode") or ""
                if "country" in address:
                    data["country"] = address.get("country") or ""

            social = data.pop("socialMedia", None)
            if isinstance(social, dict):
                for key in ("linkedin", "github", "twitter", "medium"):
                    if key in social:
                        data[key] = social.get(key) or ""

            availability = data.pop("availability", None)
            if isinstance(availability, dict):
                if "status" in availability:
                    data["availability_status"] = availability.get("status") or "available"
                if "message" in availability:
                    data["availability_message"] = availability.get("message") or ""

        return super().to_internal_value(data)
