"""Configuration de l'application Articles."""

from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    """Configuration de l'application Articles."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.articles"
    verbose_name = "Articles"

    def ready(self) -> None:
        """Enregistre l'invalidation automatique du cache."""
        from utils.cache.invalidation import register_cache_invalidation

        from .models import Article, Category, Tag

        register_cache_invalidation(Article)
        register_cache_invalidation(Category)
        register_cache_invalidation(Tag)
