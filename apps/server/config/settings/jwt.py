"""JWT and SimpleJWT configuration."""

from datetime import timedelta

from config.settings.base import DEBUG, SECRET_KEY, env

# Cle dediee (fallback SECRET_KEY) : la definir en prod isole la compromission JWT des sessions/CSRF/signatures Django.
JWT_SIGNING_KEY = env("JWT_SECRET_ACCESS_KEY", default=SECRET_KEY)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

AUTH_COOKIE_ACCESS = "access_token"
AUTH_COOKIE_REFRESH = "refresh_token"
AUTH_COOKIE_SECURE = not DEBUG
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_SAMESITE = "Strict"
AUTH_COOKIE_PATH = "/"
AUTH_COOKIE_DOMAIN = None
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 60
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 * 14
