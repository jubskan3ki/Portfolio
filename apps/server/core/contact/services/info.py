"""Service pour gerer les informations de contact."""

import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from utils.services import BaseService

from ..models import ContactInfo

logger = logging.getLogger("core.contact")

User = get_user_model()

ADMIN_BIO_CACHE_KEY = "contact:admin_bio"
ADMIN_BIO_CACHE_TTL = 60 * 30  # 30 minutes


class ContactInfoService(BaseService["ContactInfo"]):
    """Service pour les operations sur les informations de contact."""

    model = ContactInfo
    entity_name = "Information de contact"
    logger_name = "core.contact"

    @classmethod
    def get_all(cls, **_kwargs: object) -> QuerySet[ContactInfo]:
        """Recupere toutes les informations de contact."""
        return cls.model.objects.all().order_by("-is_primary", "-created_at")

    @classmethod
    def get_primary(cls) -> ContactInfo | None:
        """Recupere l'information de contact principale."""
        try:
            return cls.model.objects.get(is_primary=True)
        except ObjectDoesNotExist:
            return cls.model.objects.first()

    @classmethod
    def get_admin_bio(cls) -> str | None:
        """Recupere la bio de l'utilisateur admin (proprietaire du portfolio).

        Result is cached for 30 minutes to avoid repeated User queries.
        """
        cached = cache.get(ADMIN_BIO_CACHE_KEY)
        if cached is not None:
            return cached if cached != "" else None

        try:
            admin = User.objects.filter(is_staff=True).order_by("pk").first()
            bio = admin.bio if admin and admin.bio else None
            # Cache empty string as sentinel for "no bio" to avoid re-querying
            cache.set(ADMIN_BIO_CACHE_KEY, bio or "", ADMIN_BIO_CACHE_TTL)
            return bio
        except Exception:
            logger.exception("Erreur lors de la recuperation de la bio")
            return None

    @classmethod
    def get_public_info(cls) -> ContactInfo | dict[str, Any] | None:
        """Recupere les infos de contact pour les visiteurs publics.

        Retourne l'info primaire (a serialiser par la vue),
        un dict avec la bio admin, ou None si rien n'est disponible.
        """
        primary = cls.get_primary()
        if primary:
            return primary

        bio = cls.get_admin_bio()
        if bio:
            return {"bio": bio}

        return None
