"""JWT Cookie Authentication for Django REST Framework."""

import logging

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from utils.security.fingerprint import generate_fingerprint

logger = logging.getLogger("security")


class JWTCookieAuthentication(BaseAuthentication):
    """
    Custom authentication class that reads JWT from HTTPOnly cookies.

    This allows DRF to authenticate requests using cookies instead of
    the Authorization header, which is more secure for browser-based apps.
    Includes device fingerprint validation to prevent token theft.
    """

    def authenticate(self, request):
        """
        Authenticate the request using JWT from cookie.

        Returns a tuple of (user, token) if authentication succeeds,
        or None if no cookie is present or token is invalid.

        Validates that the request fingerprint matches the one stored in the token
        to prevent session hijacking across different browsers/devices.
        """
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

            # Validate fingerprint if present in token
            token_fingerprint = validated_token.get("fingerprint")
            if token_fingerprint:
                current_fingerprint = generate_fingerprint(request)
                if current_fingerprint.fingerprint_hash != token_fingerprint:
                    logger.warning(
                        "Fingerprint mismatch for user %s: expected %s, got %s",
                        user.pk,
                        token_fingerprint[:8],
                        current_fingerprint.fingerprint_hash[:8],
                    )
                    return None

            return (user, validated_token)

        except (InvalidToken, TokenError):
            # Token invalid or expired - return None to allow refresh flow
            return None
        except (AttributeError, TypeError, ValueError):
            return None

    def authenticate_header(self, _request):
        """
        Return a string to be used as the value of the WWW-Authenticate
        header in a 401 response.
        """
        return 'Bearer realm="api"'
