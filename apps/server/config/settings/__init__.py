"""
Django settings for portfolio project.

Settings are split into modules for better organization:
- base.py: Core Django settings
- database.py: Database configuration
- cache.py: Redis/Cache settings
- security.py: Security headers, CORS, CSRF
- rest_framework.py: DRF configuration
- jwt.py: JWT/SimpleJWT settings
- celery_conf.py: Celery configuration
- logging_conf.py: Logging configuration
- email.py: Email/SMTP settings

Usage:
    Set DJANGO_SETTINGS_MODULE=config.settings
"""

from config.settings.base import *  # noqa: F403
from config.settings.cache import *  # noqa: F403
from config.settings.celery_conf import *  # noqa: F403
from config.settings.database import *  # noqa: F403
from config.settings.email import *  # noqa: F403
from config.settings.jwt import *  # noqa: F403
from config.settings.logging_conf import *  # noqa: F403
from config.settings.rest_framework import *  # noqa: F403
from config.settings.security import *  # noqa: F403
