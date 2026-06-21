"""Utilitaires reseau."""

from typing import Any

from django.conf import settings


def get_client_ip(request: Any) -> str:
    """Retourne l'IP reelle du client derriere un proxy de confiance.

    X-Forwarded-For est une chaine "client, proxy1, ..." ou chaque proxy
    AJOUTE l'IP qu'il a vue. Les entrees de gauche sont fournies par le client
    et donc falsifiables ; seule l'entree ajoutee par notre proxy de confiance
    est fiable. Avec NUM_PROXIES proxys, on prend la NUM_PROXIES-ieme entree en
    partant de la droite (meme logique que le throttling DRF). Prendre [0]
    permettrait d'usurper l'IP (contournement/poisoning du blocage d'abus).
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        parts = [part.strip() for part in x_forwarded_for.split(",") if part.strip()]
        if parts:
            num_proxies = getattr(settings, "NUM_PROXIES", 1) or 1
            return parts[-min(num_proxies, len(parts))]
    return request.META.get("REMOTE_ADDR", "")
