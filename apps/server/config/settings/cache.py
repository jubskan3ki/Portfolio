"""Cache configuration."""

from typing import cast

from config.settings.base import env

# CACHE — Always use Redis (available in Docker stack, required for delete_pattern support)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": cast(str, env("REDIS_URL", default="redis://localhost:6379/0")),
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}
