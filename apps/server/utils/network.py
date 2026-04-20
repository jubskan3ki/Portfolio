"""Utilitaires reseau."""

from typing import Any


def get_client_ip(request: Any) -> str:
    """Retourne l'IP reelle du client, gere X-Forwarded-For derriere un proxy."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR", "")
