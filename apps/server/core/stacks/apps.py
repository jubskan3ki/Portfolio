"""Stacks app configuration."""

from django.apps import AppConfig


class StacksConfig(AppConfig):
    """Configuration de l'application des technologies et stacks."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.stacks"

    def ready(self) -> None:
        """Enregistre l'invalidation automatique du cache."""
        from utils.cache.invalidation import register_cache_invalidation

        from .models import Stack, StackCategory, StackResource

        register_cache_invalidation(Stack)
        register_cache_invalidation(StackCategory)
        register_cache_invalidation(StackResource)
