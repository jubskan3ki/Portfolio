"""Security settings - CORS, CSRF, headers."""

from config.settings.base import _ALL_INTERFACES, ALLOWED_HOSTS, DEBUG

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Nginx terminates SSL upstream
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host not in ["localhost", "127.0.0.1", "backend", "*"]
]

# CORS explicit in dev too | surfaces misconfiguration early.
CORS_ALLOW_ALL_ORIGINS = False

_DEV_ORIGINS = [
    "http://frontend:80",
    "http://swagger-ui:8080",
    "http://backend:8000",
    "http://swagger:8080",
]
_DEV_PORTS = [3000, 8000, 8085]
_DEV_HOSTS = ["localhost", _ALL_INTERFACES, "127.0.0.1"]

if DEBUG:
    CORS_ALLOWED_ORIGINS = _DEV_ORIGINS + [f"http://{host}:{port}" for host in _DEV_HOSTS for port in _DEV_PORTS]
else:
    CORS_ALLOWED_ORIGINS = []

for host in list(ALLOWED_HOSTS):
    if host not in ["localhost", "127.0.0.1", _ALL_INTERFACES, "*"] and "*" not in host:
        CORS_ALLOWED_ORIGINS.extend([f"https://{host}", f"http://{host}"])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "if-none-match",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-correlation-id",
]
CORS_EXPOSE_HEADERS = [
    "content-type",
    "content-length",
    "x-correlation-id",
    "x-request-id",
    "etag",
]
