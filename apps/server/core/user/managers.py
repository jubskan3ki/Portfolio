"""Managers pour le modele User."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import ResetPasswordCode, User

logger = logging.getLogger("core.user")


class UserManager(BaseUserManager["User"]):
    """Gestionnaire pour le modele User avec email comme identifiant."""

    def create_user(self, email: str, password: str | None = None, **extra_fields: object) -> User:
        """Cree un utilisateur avec l'email et le mot de passe fournis."""
        if not email:
            raise ValueError(_("L'adresse email est obligatoire"))

        email = self.normalize_email(email)

        # Use get_queryset for type safety instead of self.model.objects
        if self.get_queryset().filter(email=email).exists():
            logger.warning("Creation utilisateur avec email existant: %s", email)
            raise ValueError(_("Un utilisateur avec cet email existe deja"))

        user: User = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        if "date_joined" not in extra_fields:
            user.date_joined = now()

        try:
            user.save(using=self._db)
            logger.info("Utilisateur cree: %s", email)
        except Exception:
            logger.exception("Erreur creation utilisateur %s", email)
            raise
        else:
            return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: object) -> User:
        """Cree un superuser avec l'email et le mot de passe fournis."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_superuser=True."))

        # Use get_queryset for type safety instead of self.model.objects
        if self.get_queryset().filter(is_superuser=True).exists():
            logger.warning("Tentative de creation d'un second superuser")
            raise ValueError(_("Un superutilisateur existe deja."))

        logger.info("Creation superuser: %s", email)
        return self.create_user(email, password, **extra_fields)


class ResetPasswordCodeManager(models.Manager["ResetPasswordCode"]):
    """Manager pour les codes de reinitialisation de mot de passe."""

    def valid_codes(self, email: str) -> models.QuerySet[ResetPasswordCode]:
        """Retourne les codes valides (non expires, non bloques) pour un email.

        Un code est valide s'il a ete cree il y a moins de EXPIRY_MINUTES
        et n'a pas atteint le nombre maximum de tentatives.
        """
        from .models import ResetPasswordCode as ResetModel

        expiry_threshold = now() - timedelta(minutes=ResetModel.EXPIRY_MINUTES)
        return self.get_queryset().filter(
            email=email,
            created_at__gte=expiry_threshold,
            attempts__lt=ResetModel.MAX_ATTEMPTS,
        )

    def expired(self) -> models.QuerySet[ResetPasswordCode]:
        """Retourne les codes expires (pour nettoyage)."""
        from .models import ResetPasswordCode as ResetModel

        expiry_threshold = now() - timedelta(minutes=ResetModel.EXPIRY_MINUTES)
        return self.get_queryset().filter(created_at__lt=expiry_threshold)

    def for_email(self, email: str) -> models.QuerySet[ResetPasswordCode]:
        """Retourne tous les codes pour un email donne."""
        return self.get_queryset().filter(email=email)

    def cleanup_expired(self) -> int:
        """Supprime les codes expires. Retourne le nombre de codes supprimes."""
        count, _ = self.expired().delete()
        logger.info("Nettoyage codes expires: %d supprime(s)", count)
        return count
