"""Cache invalidation utilities."""

import logging
from typing import Any

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save

from utils.cache.keys import CacheKeys

logger = logging.getLogger("core.cache")


def invalidate_cache(pattern: str) -> int:
    """Requiert django-redis delete_pattern; sinon no-op."""
    try:
        if hasattr(cache, "delete_pattern"):
            count = cache.delete_pattern(pattern)
            logger.info("Invalidated %d cache keys matching: %s", count, pattern)
            return count
    except Exception as e:
        logger.warning("delete_pattern failed: %s", e)

    logger.debug("Using fallback cache invalidation for: %s", pattern)
    return 0


def invalidate_model_cache(model_name: str) -> None:
    """Invalide service-layer (CacheKeys) + view-layer (cache_page) pour un modele."""
    patterns = {
        "Article": CacheKeys.pattern_articles(),
        "Category": CacheKeys.pattern_articles(),
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
        cache.delete(CacheKeys.stats_global())
    else:
        logger.debug("No cache pattern defined for model: %s", model_name)

    view_prefixes = VIEW_CACHE_PREFIXES.get(model_name, [])
    for prefix in view_prefixes:
        invalidate_cache(f"*cache_page.{prefix}*")
        invalidate_cache(f"*cache_header.{prefix}*")


VIEW_CACHE_PREFIXES: dict[str, list[str]] = {
    "Article": [
        "portfolio:v1:views:articles:list",
        "portfolio:v1:views:articles:detail",
    ],
    "Category": ["portfolio:v1:views:articles:list"],
    "Tag": ["portfolio:v1:views:articles:list"],
    "Project": [
        "portfolio:v1:views:projects:list",
        "portfolio:v1:views:projects:detail",
    ],
    "ProjectCategory": ["portfolio:v1:views:projects:list"],
}


def clear_specific_keys(*keys: str) -> None:
    for key in keys:
        cache.delete(key)
        logger.debug("Cleared cache key: %s", key)


def clear_all_cache() -> None:
    invalidate_cache(CacheKeys.pattern_all())
    logger.info("Cleared all portfolio cache")


def _on_model_save(sender: type, **_kwargs: Any) -> None:
    invalidate_model_cache(sender.__name__)


def _on_model_delete(sender: type, **_kwargs: Any) -> None:
    invalidate_model_cache(sender.__name__)


def register_cache_invalidation(model: type) -> None:
    """Connecte post_save/post_delete signals pour invalidation auto."""
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
