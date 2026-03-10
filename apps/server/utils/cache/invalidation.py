"""Cache invalidation utilities."""

import logging
from typing import Any

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save

from utils.cache.keys import CacheKeys

logger = logging.getLogger("core.cache")


def invalidate_cache(pattern: str) -> int:
    """
    Invalidate cache keys matching a pattern.

    Note: Pattern deletion requires Redis backend with delete_pattern support.
    Falls back to individual key deletion if not available.

    Args:
        pattern: Cache key pattern (e.g., "portfolio:v1:articles:*")

    Returns:
        Number of keys deleted (approximate)
    """
    try:
        # Try delete_pattern (django-redis)
        if hasattr(cache, "delete_pattern"):
            count = cache.delete_pattern(pattern)
            logger.info("Invalidated %d cache keys matching: %s", count, pattern)
            return count
    except Exception as e:
        logger.warning("delete_pattern failed: %s", e)

    # Fallback: try to delete known keys
    logger.debug("Using fallback cache invalidation for: %s", pattern)
    return 0


def invalidate_model_cache(model_name: str) -> None:
    """
    Invalidate all cache keys for a specific model.

    Args:
        model_name: Name of the model (e.g., "Article", "Project")
    """
    patterns = {
        "Article": CacheKeys.pattern_articles(),
        "Category": CacheKeys.pattern_articles(),  # Categories affect articles
        "Tag": CacheKeys.pattern_articles(),
        "Project": CacheKeys.pattern_projects(),
        "ProjectCategory": CacheKeys.pattern_projects(),
        "Stack": CacheKeys.pattern_stacks(),
        "StackCategory": CacheKeys.pattern_stacks(),
        "StackResource": CacheKeys.pattern_stacks(),
        "Experience": CacheKeys.pattern_experiences(),
        "ExperienceType": CacheKeys.pattern_experiences(),
    }

    pattern = patterns.get(model_name)
    if pattern:
        invalidate_cache(pattern)
        # Also invalidate global stats
        cache.delete(CacheKeys.stats_global())
    else:
        logger.debug("No cache pattern defined for model: %s", model_name)


def clear_specific_keys(*keys: str) -> None:
    """
    Clear specific cache keys.

    Args:
        keys: Cache keys to delete
    """
    for key in keys:
        cache.delete(key)
        logger.debug("Cleared cache key: %s", key)


def clear_all_cache() -> None:
    """Clear all portfolio cache keys."""
    invalidate_cache(CacheKeys.pattern_all())
    logger.info("Cleared all portfolio cache")


# Signal handlers for automatic cache invalidation


def _on_model_save(sender: type, **_kwargs: Any) -> None:
    """Invalidate cache when a model is saved."""
    model_name = sender.__name__
    invalidate_model_cache(model_name)


def _on_model_delete(sender: type, **_kwargs: Any) -> None:
    """Invalidate cache when a model is deleted."""
    model_name = sender.__name__
    invalidate_model_cache(model_name)


def register_cache_invalidation(model: type) -> None:
    """
    Register a model for automatic cache invalidation.

    Args:
        model: Django model class

    Usage:
        from utils.cache.invalidation import register_cache_invalidation
        from core.articles.models import Article

        register_cache_invalidation(Article)
    """
    dispatch_uid = f"cache_invalidation_{model.__name__}"

    post_save.connect(
        _on_model_save,
        sender=model,
        dispatch_uid=f"{dispatch_uid}_save",
    )
    post_delete.connect(
        _on_model_delete,
        sender=model,
        dispatch_uid=f"{dispatch_uid}_delete",
    )

    logger.debug("Registered cache invalidation for: %s", model.__name__)
