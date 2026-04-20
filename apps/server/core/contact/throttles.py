"""Throttle personnalise pour limiter les envois de messages de contact."""

import logging
from typing import Any, cast

from django.core.cache import cache
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.throttles.base import BaseModuleThrottle

logger = logging.getLogger("core.contact")


class ContactsThrottle(BaseModuleThrottle):
    """
    Limite les requetes a la vue de contact.

    Rates:
        - GET/HEAD/OPTIONS: 30/minute (lecture)
        - POST: 5/hour (envoi de message - tres restrictif)
    """

    scope = "contact"
    read_rate = "30/minute"
    write_rate = "5/hour"

    def get_cache_key(self, request: Request, _view: APIView) -> str:
        """Genere une cle de cache incluant l'email pour les POST."""
        ident = self.get_ident(request)
        rate_type = "read" if request.method in {"GET", "HEAD", "OPTIONS"} else "write"

        if request.method == "POST" and hasattr(request, "data"):
            data = cast(dict[str, Any], request.data)
            email = data.get("email", "")
            if email:
                return f"throttle_{self.scope}_{rate_type}_{ident}_{email}"

        return f"throttle_{self.scope}_{rate_type}_{ident}"

    def allow_request(self, request: Request, view: APIView) -> bool:
        """Verifie d'abord si l'IP est bloquee pour abus avant le throttle standard."""
        ip = self.get_ident(request)
        if ip and cache.get(f"contact_abuse_blocked:{ip}"):
            self.wait_time = 86400.0
            return False
        return super().allow_request(request, view)

    def throttle_failure(self) -> bool:
        """Gere les tentatives abusives."""
        if hasattr(self, "request"):
            self._handle_abuse(self.request)
        return False

    def _handle_abuse(self, request: Request) -> None:
        """Gere les tentatives abusives de soumission."""
        ip = self.get_ident(request)
        email = "non fourni"
        if hasattr(request, "data"):
            data = cast(dict[str, Any], request.data)
            email = data.get("email", "non fourni")

        logger.warning(
            "Tentative excessive de soumission de formulaire: IP=%s, Email=%s",
            ip,
            email,
        )

        abuse_key = f"contact_abuse:{ip}"
        count: int = cache.get(abuse_key, 0) + 1
        cache.set(abuse_key, count, 86400)

        if count >= 10:
            logger.error(
                "Possible abus de formulaire: %s tentatives depuis IP=%s, Email=%s",
                count,
                ip,
                email,
            )
            cache.set(key=f"contact_abuse_blocked:{ip}", value=True, timeout=86400)
