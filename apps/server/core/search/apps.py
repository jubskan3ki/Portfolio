"""Configuration de l'application Search."""

from django.apps import AppConfig


class SearchConfig(AppConfig):
    """Configuration de l'application de recherche full-text."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.search"
    verbose_name = "Search"
