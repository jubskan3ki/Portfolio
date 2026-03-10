"""Request logging middleware.

Note: JWT authentication is handled by DRF's JWTCookieAuthentication class.
This middleware only handles request/response logging.
"""

import json
import logging
import time

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from utils.network import get_client_ip

logger = logging.getLogger("django.request")

IGNORED_PATHS = ["/static/", "/media/", "/favicon.ico", "/__debug__/"]
IGNORED_EXTENSIONS = [".css", ".js", ".ico", ".jpg", ".png", ".gif", ".svg"]
SENSITIVE_KEYS = ["password", "token", "secret", "key", "pwd"]

# RGPD: Flag pour activer/desactiver le logging d'IP
GDPR_ANONYMIZE_IP = getattr(settings, "GDPR_ANONYMIZE_IP", True)


def anonymize_ip(ip: str) -> str:
    """Anonymise une adresse IP pour conformite RGPD.

    IPv4: 192.168.1.100 -> 192.168.1.0
    IPv6: 2001:db8::1 -> 2001:db8::0
    """
    if not ip:
        return "unknown"

    if ":" in ip:
        # IPv6: masquer les 80 derniers bits (garder les 48 premiers)
        parts = ip.split(":")
        if len(parts) >= 3:
            return ":".join(parts[:3]) + "::0"
        return "ipv6:anonymized"

    # IPv4: masquer le dernier octet
    parts = ip.split(".")
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
    return "ipv4:anonymized"


def get_safe_ip(request) -> str:
    """Retourne l'IP anonymisee ou complete selon config RGPD."""
    ip = get_client_ip(request)
    if GDPR_ANONYMIZE_IP:
        return anonymize_ip(ip)
    return ip


def get_user_info(request):
    """Get user info string for logging."""
    try:
        if hasattr(request, "user") and request.user.is_authenticated:
            return f"User {request.user.id}"
    except (AttributeError, TypeError):
        pass
    return "Anonymous"


def mask_sensitive_data(data, keys=None):
    """Mask sensitive keys in data dict."""
    if keys is None:
        keys = SENSITIVE_KEYS
    if isinstance(data, dict):
        masked = data.copy()
        for key in keys:
            if key in masked:
                masked[key] = "***"
        return masked
    return data


class RequestLoggingMiddleware(MiddlewareMixin):
    """Request/response logging middleware."""

    def should_log(self, request):
        """Check if request should be logged."""
        path = request.path_info
        if any(ignored in path for ignored in IGNORED_PATHS):
            return False
        return not any(path.endswith(ext) for ext in IGNORED_EXTENSIONS)

    def process_request(self, request):
        """Log incoming request."""
        request.start_time = time.time()

        if not self.should_log(request):
            return

        logger.info(
            "[REQ] %s %s | IP: %s",
            request.method,
            request.get_full_path(),
            get_safe_ip(request),
        )

        if settings.DEBUG and request.method in ("POST", "PUT", "PATCH"):
            self._log_request_body(request)

        return

    def _log_request_body(self, request):
        """Log request body in debug mode."""
        try:
            if request.content_type == "application/json" and hasattr(request, "body"):
                body = json.loads(request.body.decode("utf-8"))
                if isinstance(body, dict):
                    logger.debug("[REQ BODY] %s", json.dumps(mask_sensitive_data(body)))
            elif request.POST:
                logger.debug("[REQ FORM] %s", mask_sensitive_data(dict(request.POST)))
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            pass

    def process_response(self, request, response):
        """Log response with timing."""
        if not self.should_log(request):
            return response

        duration = time.time() - getattr(request, "start_time", time.time())
        level = (
            logging.ERROR
            if response.status_code >= 500
            else (logging.WARNING if response.status_code >= 400 else logging.INFO)
        )

        logger.log(
            level,
            "[RESP] %s | %s %s | %s | %.3fs",
            response.status_code,
            request.method,
            request.get_full_path(),
            get_user_info(request),
            duration,
        )

        return response

    def process_exception(self, request, exception):
        """Log exceptions."""
        logger.error(
            "[EXCEPTION] %s %s | %s | %s",
            request.method,
            request.get_full_path(),
            get_user_info(request),
            exception,
            exc_info=True,
        )
        return
