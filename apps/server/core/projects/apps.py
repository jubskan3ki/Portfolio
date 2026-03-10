"""Projects app configuration."""

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """Projects app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.projects"

    def ready(self) -> None:
        """Enregistre l'invalidation automatique du cache."""
        from utils.cache.invalidation import register_cache_invalidation

        from .models import Project, ProjectCategory

        register_cache_invalidation(Project)
        register_cache_invalidation(ProjectCategory)
