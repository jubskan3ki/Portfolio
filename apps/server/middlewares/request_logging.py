"""
Middleware pour journaliser les requêtes API avec plus de détails et de performance.
"""

import logging
import time

from django.utils.deprecation import MiddlewareMixin

# Configuration du logger
logger = logging.getLogger("django.request")


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware qui enregistre les informations détaillées des requêtes API.
    """

    def process_request(self, request):
        """Log les détails de la requête entrante."""
        request.start_time = time.time()

        logger.info(
            "📡 [REQ] %s %s de l'IP %s | User-Agent: %s",
            request.method,
            request.get_full_path(),
            request.META.get("REMOTE_ADDR", "Inconnue"),
            request.META.get("HTTP_USER_AGENT", "Non spécifié"),
        )

    def process_response(self, request, response):
        """Log la réponse de la requête API avec temps de traitement."""
        duration = time.time() - getattr(request, "start_time", time.time())

        logger.info(
            "✅ [RESP] %s | %s %s (Durée: %.3fs) | Taille: %d octets",
            response.status_code,
            request.method,
            request.get_full_path(),
            duration,
            len(response.content),
        )
        return response

    def process_exception(self, request, exception):
        """Log les exceptions non gérées."""
        logger.error(
            "❌ [EXCEPTION] %s %s | Erreur: %s",
            request.method,
            request.get_full_path(),
            str(exception),
            exc_info=True,
        )
