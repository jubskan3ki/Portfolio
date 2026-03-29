"""Test settings for pytest."""

import os

from config import settings as base_settings

# Copy all uppercase settings from base settings module
for _setting_name in dir(base_settings):
    if _setting_name.isupper():
        globals()[_setting_name] = getattr(base_settings, _setting_name)

# Set environment variables for test BEFORE importing settings
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
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")


# Explicitly set ALLOWED_HOSTS to include testserver
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]


# Override database to use SQLite for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable throttling for tests by setting very high rates
# Note: Individual views still use throttle classes, so we need to define rates
REST_FRAMEWORK = dict(base_settings.REST_FRAMEWORK)
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
}

# Use console email backend for tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable CSRF and debug toolbar for testing
MIDDLEWARE = [m for m in base_settings.MIDDLEWARE if "csrf" not in m.lower() and "debug_toolbar" not in m.lower()]
INSTALLED_APPS = [app for app in base_settings.INSTALLED_APPS if app != "debug_toolbar"]

# Use local memory cache for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Disable Celery for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Speed up password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable logging during tests
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
