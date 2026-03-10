"""Cookie utilities for JWT authentication."""

import logging
from typing import Literal, cast

from django.conf import settings
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# Type alias for samesite cookie values
SameSiteType = Literal["Lax", "Strict", "None", False] | None


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    *,
    remember: bool = True,
) -> Response:
    """Set HTTPOnly cookies for JWT tokens.

    Args:
        response: DRF response object
        access_token: JWT access token
        refresh_token: JWT refresh token
        remember: If True, use persistent cookies (14 days). If False, use session cookies.
    """
    # Session cookies (None) expire when browser closes
    access_max_age = settings.AUTH_COOKIE_ACCESS_MAX_AGE if remember else None
    refresh_max_age = settings.AUTH_COOKIE_REFRESH_MAX_AGE if remember else None

    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value=access_token,
        max_age=access_max_age,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=cast(SameSiteType, settings.AUTH_COOKIE_SAMESITE),
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    response.set_cookie(
        key=settings.AUTH_COOKIE_REFRESH,
        value=refresh_token,
        max_age=refresh_max_age,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=cast(SameSiteType, settings.AUTH_COOKIE_SAMESITE),
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    return response


def set_access_cookie(response: Response, access_token: str) -> Response:
    """Set HTTPOnly cookie for access token only."""
    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value=access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=cast(SameSiteType, settings.AUTH_COOKIE_SAMESITE),
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    return response


def clear_auth_cookies(response: Response) -> Response:
    """Clear authentication cookies by setting them to expire immediately."""
    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value="",
        max_age=0,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=cast(SameSiteType, settings.AUTH_COOKIE_SAMESITE),
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    response.set_cookie(
        key=settings.AUTH_COOKIE_REFRESH,
        value="",
        max_age=0,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=cast(SameSiteType, settings.AUTH_COOKIE_SAMESITE),
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    return response


def get_access_token_from_cookie(request) -> str | None:
    """Extract access token from cookie."""
    return request.COOKIES.get(settings.AUTH_COOKIE_ACCESS)


def get_refresh_token_from_cookie(request) -> str | None:
    """Extract refresh token from cookie."""
    return request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)
