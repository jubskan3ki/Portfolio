"""Cache invalidation utilities."""

import logging
from typing import Any

from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_delete, post_save

from utils.cache.keys import CacheKeys

logger = logging.getLogger("core.cache")

# Prefixe des reponses mises en cache par ConditionalCacheMiddleware.
# Garde synchronise avec middlewares.cache.CACHE_KEY_PREFIX.
API_CACHE_PREFIX = "api_cache"

# Modele -> endpoint public dont le cache HTTP (middleware) doit etre purge.
# Permet aux mutations passant par l'admin (chemin non cacheable, donc ignore
# par l'invalidation par path du middleware) d'invalider quand meme l'api_cache.
API_CACHE_PATHS: dict[str, str] = {
    "Article": "/api/articles/",
    "Category": "/api/articles/",
    "Tag": "/api/articles/",
    "Project": "/api/projects/",
    "ProjectCategory": "/api/projects/",
    "Stack": "/api/stacks/",
    "StackCategory": "/api/stacks/",
    "StackResource": "/api/stacks/",
    "Experience": "/api/experiences/",
    "ExperienceType": "/api/experiences/",
}


def invalidate_cache(pattern: str) -> int:
    """Requiert django-redis delete_pattern; sinon no-op (loggue)."""
    try:
        if hasattr(cache, "delete_pattern"):
            count = cache.delete_pattern(pattern)
            logger.info("Invalidated %d cache keys matching: %s", count, pattern)
            return count
    except Exception as e:
        logger.warning("delete_pattern failed for %s: %s", pattern, e)
        return 0

    logger.warning("Cache backend sans delete_pattern: invalidation ignoree pour %s", pattern)
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

    # Purge aussi le cache HTTP du middleware (ConditionalCacheMiddleware) pour
    # que les mutations admin invalident l'api_cache public, pas seulement le
    # cache service-layer (cf. invalidation par signal = source de verite unique).
    api_path = API_CACHE_PATHS.get(model_name)
    if api_path:
        invalidate_cache(f"{API_CACHE_PREFIX}:{api_path}*")


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
    from utils.signals import bulk_mode_active

    # Import en masse : invalidation par-objet desactivee ; l'appelant invalide
    # en bloc apres l'import via invalidate_model_cache (cf. utils.signals).
    if bulk_mode_active():
        return
    # on_commit: n'invalide qu'apres COMMIT pour eviter qu'une lecture
    # concurrente repeuple le cache avec les anciennes donnees (et pour ne
    # rien invalider si la transaction rollback). Hors transaction, le callback
    # s'execute immediatement.
    name = sender.__name__
    transaction.on_commit(lambda: invalidate_model_cache(name))


def _on_model_delete(sender: type, **_kwargs: Any) -> None:
    from utils.signals import bulk_mode_active

    if bulk_mode_active():
        return
    name = sender.__name__
    transaction.on_commit(lambda: invalidate_model_cache(name))


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
