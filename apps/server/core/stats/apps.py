"""Configuration de l'application Stats."""

from django.apps import AppConfig


class StatsConfig(AppConfig):
    """Configuration de l'application Stats."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.stats"
    verbose_name = "Stats"
