"""
Configuration de l'application Contact.
"""

from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Configuration de l'application Contact.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.contact"

    def ready(self) -> None:
        # Enregistre les signaux (invalidation du cache de la bio admin).
        from . import signals  # noqa: F401
