"""Security middleware for API protection."""

import json
import logging
import re
import secrets
import time

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from utils.network import get_client_ip

logger = logging.getLogger("django.security")

# Admin login rate limiting: max attempts per IP within window
_ADMIN_LOGIN_MAX_ATTEMPTS = 5
_ADMIN_LOGIN_WINDOW = 300  # 5 minutes
_admin_login_attempts: dict[str, list[float]] = {}

BLOCKED_IPS: set[str] = getattr(settings, "BLOCKED_IPS", set())
BLOCKED_USER_AGENTS: set[str] = getattr(settings, "BLOCKED_USER_AGENTS", {"BadBot", "MaliciousScraper", "Pykek"})
BLOCKED_METHODS: set[str] = getattr(settings, "BLOCKED_METHODS", {"TRACE", "TRACK"})

DEFAULT_SUSPICIOUS_PATTERNS = [
    r"(?i)../../",
    r"(?i)select.+from.+where",
    r"(?i)union\s+select",
    r"(?i)eval\s*\(",
    r"(?i)<script>",
    r"(?i)javascript:",
    r"(?i)onerror=",
    r"(?i)/etc/passwd",
]

SUSPICIOUS_PATTERNS = getattr(settings, "SUSPICIOUS_PATTERNS", DEFAULT_SUSPICIOUS_PATTERNS)

# Combine all patterns into a single compiled regex (1 search() instead of N)
_SUSPICIOUS_RE = re.compile(
    "|".join(p[4:] if p.startswith("(?i)") else p for p in SUSPICIOUS_PATTERNS),
    re.IGNORECASE,
)

# Skip JSON body scan beyond this size (large uploads/imports, not injections)
_MAX_BODY_SCAN_SIZE = 65_536  # 64 KB


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to responses."""

    def process_response(self, request, response):
        """Add security headers."""
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response["X-XSS-Protection"] = "1; mode=block"

        if not settings.DEBUG:
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        if hasattr(request, "csp_nonce"):
            response["Content-Security-Policy"] = f"script-src 'self' 'nonce-{request.csp_nonce}'"

        return response


class SecurityMiddleware(MiddlewareMixin):
    """Advanced security middleware for request validation."""

    def process_request(self, request):
        """Validate incoming requests."""
        ip = get_client_ip(request)

        # Rate limit admin login attempts
        if request.path == "/admin/login/" and request.method == "POST":
            now = time.monotonic()
            attempts = _admin_login_attempts.get(ip, [])
            attempts = [t for t in attempts if now - t < _ADMIN_LOGIN_WINDOW]
            if len(attempts) >= _ADMIN_LOGIN_MAX_ATTEMPTS:
                logger.warning("Admin login rate limited: %s", ip)
                msg = "Too many attempts. Try again later."
                return JsonResponse(
                    {"errors": [{"code": "rate_limited", "message": msg}]},
                    status=429,
                )
            attempts.append(now)
            _admin_login_attempts[ip] = attempts

        if ip in BLOCKED_IPS:
            logger.warning("Blocked IP: %s", ip)
            return JsonResponse(
                {"errors": [{"code": "access_denied", "message": "Access denied."}]},
                status=403,
            )

        user_agent = request.META.get("HTTP_USER_AGENT", "")
        for blocked in BLOCKED_USER_AGENTS:
            if blocked in user_agent:
                logger.warning("Blocked user agent: %s", user_agent)
                return JsonResponse(
                    {"errors": [{"code": "access_denied", "message": "Access denied."}]},
                    status=403,
                )

        if request.method in BLOCKED_METHODS:
            logger.warning("Blocked method: %s", request.method)
            return JsonResponse(
                {"errors": [{"code": "method_not_allowed", "message": f"Method {request.method} not allowed."}]},
                status=405,
            )

        if self._has_suspicious_content(request):
            logger.warning("Suspicious content detected")
            return JsonResponse(
                {"errors": [{"code": "request_blocked", "message": "Request blocked."}]},
                status=400,
            )

        if not settings.DEBUG:
            request.csp_nonce = secrets.token_hex(16)

        return None

    def _has_suspicious_content(self, request):
        """Check for suspicious patterns in request."""
        for key, value in request.GET.items():
            if self._is_suspicious(key) or self._is_suspicious(value):
                return True

        if request.method in ("POST", "PUT", "PATCH"):
            for key, value in request.POST.items():
                if self._is_suspicious(key) or self._is_suspicious(value):
                    return True

            if "application/json" in request.content_type and len(request.body) <= _MAX_BODY_SCAN_SIZE:
                try:
                    body = json.loads(request.body.decode("utf-8"))
                    if self._check_json(body):
                        return True
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # JSON malformé = erreur client, pas une attaque ; laisser DRF gérer
                    return False

        return False

    @staticmethod
    def _is_suspicious(text):
        """Check if text matches suspicious patterns."""
        if not text or not isinstance(text, str):
            return False
        return bool(_SUSPICIOUS_RE.search(text))

    def _check_json(self, data, depth=0):
        """Recursively check JSON for suspicious patterns."""
        if depth > 3:
            return False

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(key, str) and self._is_suspicious(key):
                    return True
                if isinstance(value, (dict, list)):
                    if self._check_json(value, depth + 1):
                        return True
                elif isinstance(value, str) and self._is_suspicious(value):
                    return True

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    if self._check_json(item, depth + 1):
                        return True
                elif isinstance(item, str) and self._is_suspicious(item):
                    return True

        return False
