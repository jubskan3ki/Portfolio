"""
Middleware de sécurité avancé pour protéger l'API contre les abus.
"""

import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# Logger pour les alertes de sécurité
security_logger = logging.getLogger("django.security")

# Liste des IP interdites (peut être mise à jour dynamiquement)
BLOCKED_IPS = {"192.168.1.100", "10.0.0.50"}

# Liste des User-Agents interdits (exemple de bots malveillants)
BLOCKED_USER_AGENTS = {"BadBot", "MaliciousScraper"}

# Liste des méthodes HTTP interdites (ex: suppression globale non autorisée)
BLOCKED_METHODS = {"TRACE", "TRACK"}


class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware de sécurité avancé pour restreindre les accès API.
    """

    def process_request(self, request):
        """Blocage des requêtes suspectes basées sur IP, User-Agent et méthode HTTP."""

        # Vérification des IP bloquées
        ip = request.META.get("REMOTE_ADDR")
        if ip in BLOCKED_IPS:
            security_logger.warning("🚨 IP bloquée: %s - Accès refusé", ip)
            return JsonResponse(
                {"error": "Accès refusé depuis cette adresse IP."},
                status=403,
            )

        # Vérification des User-Agents interdits
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        for blocked_agent in BLOCKED_USER_AGENTS:
            if blocked_agent in user_agent:
                security_logger.warning("🚨 Bot suspect détecté: %s - Requête bloquée", user_agent)
                return JsonResponse(
                    {"error": "Accès interdit. User-Agent non autorisé."},
                    status=403,
                )

        # Vérification des méthodes HTTP interdites
        if request.method in BLOCKED_METHODS:
            security_logger.warning("🚨 Méthode HTTP interdite: %s - Bloquée", request.method)
            return JsonResponse(
                {"error": f"Méthode HTTP {request.method} non autorisée."},
                status=405,
            )

    def process_response(self, response):
        """Ajout d'en-têtes de sécurité renforcés pour l'API."""
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response
