"""Service d'authentification administrateur."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from utils.exceptions import AuthenticationError, NotFoundError

if TYPE_CHECKING:
    from core.user.models import User as UserType

logger = logging.getLogger("core.user")
User = get_user_model()


class AdminService:
    """Service pour l'authentification des administrateurs."""

    @staticmethod
    def login_user(email: str, password: str, session_id: str | None = None) -> dict[str, Any]:
        """Authentifie un admin et retourne ses tokens JWT.

        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            session_id: Identifiant unique de la session (propage dans le JWT)

        Returns:
            Dictionnaire contenant les tokens et l'utilisateur
        """
        user = authenticate(username=email, password=password)

        if not user:
            logger.warning("Connexion echouee pour %s", email)
            raise AuthenticationError("Identifiants invalides.")

        if not user.is_active:
            logger.warning("Compte desactive: %s", email)
            raise AuthenticationError("Ce compte est desactive.")

        if not user.is_staff or not user.is_superuser:
            logger.warning("Compte non admin: %s", email)
            raise AuthenticationError("Ce compte n'a pas les permissions requises.")

        refresh = RefreshToken.for_user(user)

        if session_id:
            refresh["session_id"] = session_id
            refresh.access_token["session_id"] = session_id

        logger.info("Connexion reussie pour %s", email)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user,
        }

    @staticmethod
    def get_admin_profile(user_id: int) -> UserType:
        """Recupere le profil administrateur."""
        try:
            return User.objects.get(id=user_id, is_staff=True, is_superuser=True)
        except User.DoesNotExist as exc:
            logger.exception("Profil admin inexistant: %s", user_id)
            raise NotFoundError("Profil administrateur non trouve.") from exc

    @staticmethod
    def update_admin_profile(user_id: int, profile_data: dict[str, Any]) -> UserType:
        """Met a jour le profil administrateur."""
        try:
            user = User.objects.get(id=user_id, is_staff=True, is_superuser=True)

            for key, value in profile_data.items():
                setattr(user, key, value)

            user.save()
            logger.info("Profil admin mis a jour: %s", user.email)

        except User.DoesNotExist as exc:
            logger.exception("Mise a jour profil admin inexistant: %s", user_id)
            raise NotFoundError("Profil administrateur non trouve.") from exc
        else:
            return user
