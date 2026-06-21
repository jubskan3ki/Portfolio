"""Service d'authentification administrateur."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from utils.exceptions import AuthenticationError, NotFoundError, ValidationError
from utils.security import SessionManager

if TYPE_CHECKING:
    from core.user.models import User as UserType

logger = logging.getLogger("core.user")
User = get_user_model()


class AdminService:
    """Service pour l'authentification des administrateurs."""

    # Liste blanche pour bloquer l'escalade de privileges meme si le serializer laisse passer un champ sensible.
    ALLOWED_PROFILE_FIELDS: frozenset[str] = frozenset(
        {
            "first_name",
            "last_name",
            "phone_number",
            "bio",
            "avatar",
            "position",
            "public_email",
            "linkedin",
            "github",
        }
    )

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
    def refresh_session(refresh_token_str: str) -> dict[str, Any]:
        """Valide et rafraichit une session JWT admin.

        Verifie la session associee au refresh token, gere la rotation et le
        blacklist eventuels, puis retourne les nouveaux tokens. La pose des
        cookies reste a la charge de la vue.

        Args:
            refresh_token_str: Refresh token brut issu du cookie/body.

        Returns:
            Dictionnaire avec "access" (str) et "refresh" (str | None : present
            uniquement si la rotation est active).

        Raises:
            AuthenticationError: session invalide/revoquee, utilisateur introuvable
                ou token invalide/expire (cas 401).
        """
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError as exc:
            raise AuthenticationError("Token invalide ou expire") from exc

        token_session_id = refresh_token.get("session_id")
        token_user_id = refresh_token.get("user_id")

        if not token_session_id or not token_user_id:
            raise AuthenticationError("Session invalide")

        if not SessionManager(token_user_id).is_session_valid(str(token_session_id)):
            logger.info("Refresh refuse: session %s revoquee", str(token_session_id)[:8])
            raise AuthenticationError("Session revoquee")

        new_access_token = str(refresh_token.access_token)
        new_refresh_token = None

        simple_jwt_settings = getattr(settings, "SIMPLE_JWT", {})
        if simple_jwt_settings.get("ROTATE_REFRESH_TOKENS", False):
            if simple_jwt_settings.get("BLACKLIST_AFTER_ROTATION", False):
                try:
                    refresh_token.blacklist()
                except AttributeError:
                    logger.exception(
                        "Token blacklist method unavailable - "
                        "check rest_framework_simplejwt.token_blacklist is in INSTALLED_APPS"
                    )
                except TokenError:
                    logger.exception("Failed to blacklist rotated refresh token")
            try:
                user = User.objects.get(id=token_user_id)
            except User.DoesNotExist as exc:
                raise AuthenticationError("Utilisateur introuvable") from exc
            new_refresh = RefreshToken.for_user(user)

            if token_session_id:
                new_refresh["session_id"] = token_session_id
                new_refresh.access_token["session_id"] = token_session_id

            new_refresh_token = str(new_refresh)

        return {
            "access": new_access_token,
            "refresh": new_refresh_token,
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

            updated_fields = [key for key in profile_data if key in AdminService.ALLOWED_PROFILE_FIELDS]
            for key in updated_fields:
                setattr(user, key, profile_data[key])

            # full_clean execute les validateurs modele (dont validate_image_upload), court-circuites par setattr + save().
            user.full_clean(exclude=[f.name for f in user._meta.fields if f.name not in updated_fields])
            user.save(update_fields=[*updated_fields, "updated_at"] if updated_fields else None)
            logger.info("Profil admin mis a jour: %s", user.email)

        except User.DoesNotExist as exc:
            logger.exception("Mise a jour profil admin inexistant: %s", user_id)
            raise NotFoundError("Profil administrateur non trouve.") from exc
        except DjangoValidationError as exc:
            logger.warning("Validation profil admin echouee: %s", user_id)
            raise ValidationError(exc.messages[0] if exc.messages else "Donnees invalides.") from exc
        else:
            return user
