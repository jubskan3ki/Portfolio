"""Middleware de detection et suivi des appareils."""

import logging
from typing import Any

from django.utils.deprecation import MiddlewareMixin

from utils.security import extract_device_info, generate_fingerprint, get_session_manager

logger = logging.getLogger("security")


def get_session_id_from_request(request: Any) -> str | None:
    """Recupere l'ID de session depuis le fingerprint du JWT.

    Le fingerprint est stocke dans le token lors du login et sert
    d'identifiant unique de session par appareil/navigateur.

    Args:
        request: Objet request Django.

    Returns:
        Le fingerprint hash ou None.
    """
    auth = getattr(request, "auth", None)
    if auth:
        fingerprint = auth.get("fingerprint")
        if fingerprint:
            return str(fingerprint)
    return None


class DeviceTrackingMiddleware(MiddlewareMixin):
    """Middleware pour tracker les appareils et gerer les sessions."""

    def process_request(self, request: Any) -> None:
        """Extrait les informations de l'appareil et gere la session."""
        # Extraire les informations de l'appareil
        fingerprint = generate_fingerprint(request)
        device_info: dict[str, Any] = extract_device_info(request)
        request.device_info = device_info
        request.fingerprint = fingerprint

        # Gerer la session si l'utilisateur est authentifie
        if not self._is_authenticated(request):
            return

        session_manager = get_session_manager(request.user)
        if not session_manager:
            return

        # Use fingerprint hash as session ID (consistent with login)
        session_id = fingerprint.fingerprint_hash

        # Update session activity
        session_manager.update_activity(session_id)

        request.session_manager = session_manager
        request.session_id = session_id

    def _is_authenticated(self, request: Any) -> bool:
        """Verifie si l'utilisateur est authentifie."""
        user = getattr(request, "user", None)
        return user is not None and getattr(user, "is_authenticated", False)
