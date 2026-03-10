"""Utilitaires de securite avances."""

from .cookies import (
    clear_auth_cookies,
    get_access_token_from_cookie,
    get_refresh_token_from_cookie,
    set_access_cookie,
    set_auth_cookies,
)
from .fingerprint import DeviceFingerprint, extract_device_info, generate_fingerprint
from .jwt_cookie_auth import JWTCookieAuthentication
from .sessions import SessionManager, get_session_manager

__all__ = [
    "DeviceFingerprint",
    "JWTCookieAuthentication",
    "SessionManager",
    "clear_auth_cookies",
    "extract_device_info",
    "generate_fingerprint",
    "get_access_token_from_cookie",
    "get_refresh_token_from_cookie",
    "get_session_manager",
    "set_access_cookie",
    "set_auth_cookies",
]
