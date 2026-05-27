"""Test settings for pytest."""

import os

# django-environ reads env at settings import | must be set first.
os.environ.setdefault("JWT_SECRET_ACCESS_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
os.environ.setdefault("SMTP_HOST", "localhost")
os.environ.setdefault("SMTP_PORT", "25")
os.environ.setdefault("SMTP_USER", "test")
os.environ.setdefault("SMTP_PASS", "test")
os.environ.setdefault("EMAIL_FROM", "test@example.com")
os.environ.setdefault("ADMIN_EMAIL", "admin@example.com")
os.environ.setdefault("ADMIN_PASSWORD", "testpassword123")
os.environ.setdefault("DB_NAME", "portfolio_db")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")
os.environ.setdefault("DB_HOST", "postgres-db")
os.environ.setdefault("DB_PORT", "5432")
os.environ["USE_S3"] = "false"

from config import settings as base_settings
from config.settings.base import INSTALLED_APPS as _BASE_INSTALLED_APPS
from config.settings.base import MIDDLEWARE as _BASE_MIDDLEWARE
from config.settings.rest_framework import REST_FRAMEWORK as _BASE_REST_FRAMEWORK

for _setting_name in dir(base_settings):
    if _setting_name.isupper():
        globals()[_setting_name] = getattr(base_settings, _setting_name)


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]


# PostgreSQL (not SQLite) | exercise real extensions (unaccent/pg_trgm), triggers, GIN indexes.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "portfolio_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("TEST_DB_HOST", "postgres-db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "TEST": {"NAME": f"test_{os.environ.get('DB_NAME', 'portfolio_db')}"},
    }
}

# High rates effectively disable throttling; views still reference keys so they must exist.
REST_FRAMEWORK = dict(_BASE_REST_FRAMEWORK)
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "10000/minute",
    "user": "10000/minute",
    "login": "10000/minute",
    "reset_password": "10000/minute",
    "change_password": "10000/minute",
    "sessions": "10000/minute",
    "stack": "10000/minute",
    "projects": "10000/minute",
    "experience": "10000/minute",
    "article": "10000/minute",
    "articles": "10000/minute",
    "article_view": "10000/minute",
    "contact": "10000/minute",
    "web_vitals": "10000/minute",
    "webhooks": "10000/minute",
    "stats": "10000/minute",
    "audit": "10000/minute",
    "transfer": "10000/minute",
    "search": "10000/minute",
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

MIDDLEWARE = [m for m in _BASE_MIDDLEWARE if "csrf" not in m.lower() and "debug_toolbar" not in m.lower()]
INSTALLED_APPS = [app for app in _BASE_INSTALLED_APPS if app != "debug_toolbar"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {"class": "logging.NullHandler"},
    },
    "root": {
        "handlers": ["null"],
        "level": "CRITICAL",
    },
}
