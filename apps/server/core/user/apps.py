"""
Configuration de l'application User.
"""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """Configuration de l'application utilisateur."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.user"
