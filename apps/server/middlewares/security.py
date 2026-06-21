"""Security middleware for API protection."""

import json
import logging
import re
import secrets

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from utils.network import get_client_ip

logger = logging.getLogger("django.security")

# Admin login rate limiting: max attempts per IP within window.
# Compteur stocké dans Redis (TTL = fenêtre) : borné en mémoire et partagé
# entre tous les workers, contrairement à un dict module-level par process.
_ADMIN_LOGIN_MAX_ATTEMPTS = 5
_ADMIN_LOGIN_WINDOW = 300  # 5 minutes

BLOCKED_IPS: set[str] = getattr(settings, "BLOCKED_IPS", set())
BLOCKED_USER_AGENTS: set[str] = getattr(settings, "BLOCKED_USER_AGENTS", {"BadBot", "MaliciousScraper", "Pykek"})
BLOCKED_METHODS: set[str] = getattr(settings, "BLOCKED_METHODS", {"TRACE", "TRACK"})

DEFAULT_SUSPICIOUS_PATTERNS = [
    r"(?i)\.\./\.\./",
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
        # X-XSS-Protection: 0 = recommandation moderne (le filtre XSS legacy des
        # navigateurs introduisait lui-meme des vulns ; on s'appuie sur la CSP).
        response["X-XSS-Protection"] = "0"

        if not settings.DEBUG:
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        if hasattr(request, "csp_nonce"):
            response["Content-Security-Policy"] = self._build_csp(request.csp_nonce)

        return response

    @staticmethod
    def _build_csp(nonce: str) -> str:
        """Construit une CSP restrictive.

        script-src reste limite a 'self' + nonce (pas d'unsafe-inline). style-src
        garde 'unsafe-inline' pour ne pas casser les styles inline de l'admin
        Django (risque XSS via CSS marginal compare aux scripts). Les directives
        structurelles (object/base/frame-ancestors) verrouillent le reste.
        """
        return "; ".join(
            [
                "default-src 'self'",
                f"script-src 'self' 'nonce-{nonce}'",
                "style-src 'self' 'unsafe-inline'",
                "img-src 'self' data:",
                "font-src 'self'",
                "connect-src 'self'",
                "object-src 'none'",
                "base-uri 'none'",
                "frame-ancestors 'none'",
                "form-action 'self'",
            ]
        )


class SecurityMiddleware(MiddlewareMixin):
    """Advanced security middleware for request validation."""

    def process_request(self, request):
        """Validate incoming requests."""
        ip = get_client_ip(request)

        # Rate limit admin login attempts (compteur Redis avec TTL = fenêtre).
        # Django admin est monté sur /django-admin/ (cf. config/urls.py) ; /admin/
        # est la SPA Nuxt et ne touche jamais ce backend. On vise donc le vrai
        # chemin de login, sinon le brute-force Django admin n'est pas limité.
        if request.path == "/django-admin/login/" and request.method == "POST":
            cache_key = f"admin_login_attempts:{ip}"
            attempts = cache.get_or_set(cache_key, 0, _ADMIN_LOGIN_WINDOW) or 0
            if attempts >= _ADMIN_LOGIN_MAX_ATTEMPTS:
                logger.warning("Admin login rate limited: %s", ip)
                msg = "Too many attempts. Try again later."
                return JsonResponse(
                    {"errors": [{"code": "rate_limited", "message": msg}]},
                    status=429,
                )
            try:
                # incr préserve le TTL posé par get_or_set (fenêtre fixe).
                cache.incr(cache_key)
            except ValueError:
                # La clé a expiré entre get_or_set et incr : on repart à 1.
                cache.set(cache_key, 1, _ADMIN_LOGIN_WINDOW)

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
                if isinstance(value, dict | list):
                    if self._check_json(value, depth + 1):
                        return True
                elif isinstance(value, str) and self._is_suspicious(value):
                    return True

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict | list):
                    if self._check_json(item, depth + 1):
                        return True
                elif isinstance(item, str) and self._is_suspicious(item):
                    return True

        return False
