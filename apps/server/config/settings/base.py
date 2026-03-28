"""Core Django settings."""

import ipaddress
from pathlib import Path
from typing import cast

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_DEBUG=(bool, False),
    SMTP_HOST=(str, ""),
    SMTP_PORT=(str, "587"),
    REDIS_URL=(str, "redis://redis:6379/1"),
    CELERY_BROKER_URL=(str, ""),
    ENABLE_DEBUG_TOOLBAR=(bool, True),
)
environ.Env.read_env(BASE_DIR / ".env")

# CORE SETTINGS

SECRET_KEY = cast(str, env("DJANGO_SECRET_KEY"))
DEBUG = cast(bool, env.bool("DJANGO_DEBUG"))
ENABLE_DEBUG_TOOLBAR = DEBUG and cast(bool, env.bool("ENABLE_DEBUG_TOOLBAR"))
ALLOWED_HOSTS = cast(list, env.list("ALLOWED_HOSTS"))
if DEBUG and "0.0.0.0" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("0.0.0.0")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "user.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# APPLICATIONS

INSTALLED_APPS = [
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_extensions",
    "django_filters",
    "drf_spectacular",
    *(["debug_toolbar"] if ENABLE_DEBUG_TOOLBAR else []),
    "core.user.apps.UserConfig",
    "core.articles.apps.ArticlesConfig",
    "core.contact.apps.ContactConfig",
    "core.experiences.apps.ExperiencesConfig",
    "core.projects.apps.ProjectsConfig",
    "core.stacks.apps.StacksConfig",
    "core.transfer.apps.TransferConfig",
    "core.stats.apps.StatsConfig",
    "core.audit.apps.AuditConfig",
    "core.webhooks.apps.WebhooksConfig",
]

# MIDDLEWARE

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "middlewares.correlation.CorrelationIdMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "middlewares.auth.RequestLoggingMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core.audit.middleware.AuditContextMiddleware",
    "middlewares.device.DeviceTrackingMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middlewares.cache.ConditionalCacheMiddleware",
    *(["debug_toolbar.middleware.DebugToolbarMiddleware"] if ENABLE_DEBUG_TOOLBAR else []),
    *(
        [
            "middlewares.security.SecurityHeadersMiddleware",
            "middlewares.security.SecurityMiddleware",
        ]
        if not DEBUG
        else []
    ),
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# TEMPLATES

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# STATIC & MEDIA FILES

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CUSTOM SETTINGS

HTML_COMPRESSION_EXCLUDE_PATHS = ["/admin/", "/__debug__/"]

# Session & Device Management
MAX_SESSIONS_PER_USER = 5
SESSION_TIMEOUT = 24 * 60 * 60  # 24 heures en secondes
DEVICE_TRACKING_ENABLED = True

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# Upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 5_242_880  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5_242_880  # 5 MB

# DEBUG TOOLBAR (Development only)


def show_toolbar(request) -> bool:
    """Affiche la toolbar uniquement pour localhost et reseau Docker local."""

    if not ENABLE_DEBUG_TOOLBAR:
        return False

    remote_addr = request.META.get("REMOTE_ADDR", "")
    if not remote_addr:
        return False

    try:
        client_ip = ipaddress.ip_address(remote_addr)
    except ValueError:
        return False

    allowed_networks = [
        ipaddress.ip_network("127.0.0.0/8"),
        ipaddress.ip_network("::1/128"),
        ipaddress.ip_network("172.16.0.0/12"),
    ]
    return any(client_ip in network for network in allowed_networks)


if ENABLE_DEBUG_TOOLBAR:
    INTERNAL_IPS = ["127.0.0.1", "::1", "172.17.0.1"]
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": "config.settings.base.show_toolbar",
    }

# UPLOAD CONSTRAINTS

ALLOWED_AVATAR_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
