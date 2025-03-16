"""
User app configuration
"""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Configuration de l'application User.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.user"

    def ready(self):
        """
        Cette méthode est appelée automatiquement
        lors du chargement de l'application User.
        Elle permet d'enregistrer les signaux.
        """
        # pylint: disable=import-outside-toplevel, unused-import
        from . import signals
