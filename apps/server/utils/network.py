"""
Utilitaires reseau pour l'application.
Fournit des fonctions pour la gestion des adresses IP et autres operations reseau.
"""

from typing import Any


def get_client_ip(request: Any) -> str:
    """
    Obtient l'adresse IP reelle du client, meme derriere un proxy.

    Cette fonction gere les cas ou l'application est derriere un reverse proxy
    (Nginx, Apache, load balancer) en verifiant l'en-tete X-Forwarded-For.

    Args:
        request: La requete HTTP Django

    Returns:
        str: L'adresse IP du client
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    # Format X-Forwarded-For: client, proxy1, proxy2, ...
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR", "")
