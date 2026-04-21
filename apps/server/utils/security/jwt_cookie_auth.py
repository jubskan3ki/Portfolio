"""JWT Cookie Authentication for Django REST Framework."""

import logging

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from utils.security.sessions import SessionManager

logger = logging.getLogger("security")


class JWTCookieAuthentication(BaseAuthentication):
    """Authentification JWT via cookie HTTPOnly pour DRF.

    Rejette le token si la session associee (claim `session_id`) n'existe
    plus dans le SessionManager, afin qu'une revocation cote admin deconnecte
    immediatement l'appareil concerne.
    """

    def authenticate(self, request):
        """Authentifie la requete en lisant le JWT depuis le cookie."""
        cookie_name = getattr(settings, "AUTH_COOKIE_ACCESS", "access_token")
        raw_token = request.COOKIES.get(cookie_name)

        if not raw_token:
            return None

        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(raw_token)
            user = jwt_auth.get_user(validated_token)

            if not user or not user.is_authenticated:
                return None

            session_id = validated_token.get("session_id")
            if not session_id:
                logger.warning("JWT sans session_id rejete pour user %s", user.pk)
                return None

            if not SessionManager(user.pk).is_session_valid(str(session_id)):
                logger.info("Session %s invalide/revoquee pour user %s", str(session_id)[:8], user.pk)
                return None

            return (user, validated_token)

        except (InvalidToken, TokenError):
            return None
        except (AttributeError, TypeError, ValueError):
            return None

    def authenticate_header(self, _request):
        """En-tete WWW-Authenticate pour les reponses 401."""
        return 'Bearer realm="api"'
