"""JWT and SimpleJWT configuration."""

from datetime import timedelta

from config.settings.base import DEBUG, SECRET_KEY

# JWT SETTINGS

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# Cookie settings for JWT authentication
AUTH_COOKIE_ACCESS = "access_token"
AUTH_COOKIE_REFRESH = "refresh_token"
AUTH_COOKIE_SECURE = not DEBUG
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_SAMESITE = "Strict"
AUTH_COOKIE_PATH = "/"
AUTH_COOKIE_DOMAIN = None
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 60  # 1 hour
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 * 14  # 14 days
