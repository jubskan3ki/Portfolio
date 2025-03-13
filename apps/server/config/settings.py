"""
Configuration principale du projet Django.
Gère les paramètres globaux de l'application, y compris la base de données,
les fichiers statiques, l'authentification et le middleware.
"""

from pathlib import Path

import environ

# 📝 Configuration des applications de l'administrateur
AUTH_USER_MODEL = "user.User"

# 📌 Définition du répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Init environ
env = environ.Env(DEBUG=(bool, False))
# ✅ Charge les variables depuis l'environnement Docker
environ.Env.read_env(BASE_DIR / ".env")

# 🔐 Clé secrète et mode debug
SECRET_KEY = env("JWT_SECRET_ACCESS_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# 🌍 Configuration des hôtes autorisés
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# 📂 Configuration des templates
ROOT_URLCONF = "config.urls"

# 📁 Configuration des fichiers statiques et médias
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 🌐 Paramètres internationaux
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# 🔑 Type de clé primaire par défaut pour les modèles
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 🚀 WSGI et ASGI Application
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# 🔐 Sécurité Nginx
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# 📧 Paramètres de l'administrateur
ADMIN_USER = env("ADMIN_EMAIL")
ADMIN_PASSWORD = env("ADMIN_PASSWORD")

# 📧 Paramètres de l'email (Utilisation des variables d'environnement)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("SMTP_HOST")
EMAIL_PORT = int(env("SMTP_PORT").strip())
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("SMTP_USER")
EMAIL_HOST_PASSWORD = env("SMTP_PASS")
DEFAULT_FROM_EMAIL = env("EMAIL_FROM")

# Broker RabbitMQ
CELERY_BROKER_URL = env("CELERY_BROKER_URL")

# Format recommandé
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Toujours bon d’avoir une timezone uniforme
CELERY_TIMEZONE = "Europe/Paris"

# 🛠️ Configuration de la base de données
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

# 📝 Configuration des logs (Django attend une **chaîne**, pas un dict)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django_errors.log",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# 🏗️ Applications installées
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_extensions",
    "debug_toolbar",
    "core.user.apps.UserConfig",
    "core.blog.apps.BlogConfig",
    "core.contact.apps.ContactConfig",
    "core.experience.apps.ExperienceConfig",
    "core.projects.apps.ProjectsConfig",
    "core.stacks.apps.StacksConfig",
]


# 🔄 Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "middlewares.request_logging.RequestLoggingMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


# 📝 Context Processors
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

# 🔐 Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.CustomPagination",
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
    "PAGE_SIZE": 10,
}

# 🌐 Configuration de l'Auth
AUTHENTICATION_BACKENDS = [
    "core.user.authentication.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]
