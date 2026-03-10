"""Experience app configuration."""

from django.apps import AppConfig


class ExperiencesConfig(AppConfig):
    """Experience app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.experiences"

    def ready(self) -> None:
        """Enregistre l'invalidation automatique du cache."""
        from utils.cache.invalidation import register_cache_invalidation

        from .models import Experience, ExperienceType

        register_cache_invalidation(Experience)
        register_cache_invalidation(ExperienceType)
