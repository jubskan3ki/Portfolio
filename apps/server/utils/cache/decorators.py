"""Cache decorators for service methods."""

import hashlib
import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from django.core.cache import cache

from utils.cache.keys import CacheKeys

logger = logging.getLogger("core.cache")

P = ParamSpec("P")
R = TypeVar("R")


def cached_queryset(
    cache_key: str | Callable[..., str],
    timeout: int = CacheKeys.TTL_MEDIUM,
    serializer: Callable[[object], object] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to cache queryset results.

    Args:
        cache_key: Static key string or callable that returns key from args
        timeout: Cache timeout in seconds
        serializer: Optional function to serialize queryset before caching

    Usage:
        @cached_queryset(CacheKeys.article_featured, timeout=300)
        def get_featured(limit: int = 5):
            return Article.objects.featured()[:limit]

        @cached_queryset(lambda slug: CacheKeys.article_detail(slug), timeout=600)
        def get_by_slug(slug: str):
            return Article.objects.get(slug=slug)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Generate cache key
            if callable(cache_key):
                try:
                    # Try to call with the same args
                    key = cache_key(*args[1:], **kwargs)  # Skip self for methods
                except TypeError:
                    key = cache_key(**kwargs)
            else:
                key = cache_key

            # Try to get from cache
            cached = cache.get(key)
            if cached is not None:
                logger.debug("Cache hit: %s", key)
                return cached

            # Call the actual function
            logger.debug("Cache miss: %s", key)
            result = func(*args, **kwargs)

            # Serialize if needed
            if serializer and result is not None:
                try:
                    cache_value = serializer(result)
                except Exception as e:
                    logger.warning("Failed to serialize for cache: %s", e)
                    return result
            else:
                # Convert queryset to list for caching
                cache_value = list(result) if hasattr(result, "__iter__") and hasattr(result, "model") else result

            # Store in cache
            cache.set(key, cache_value, timeout)
            logger.debug("Cached: %s (timeout=%ds)", key, timeout)

            return result

        return wrapper

    return decorator


def cached_method(
    key_prefix: str,
    timeout: int = CacheKeys.TTL_MEDIUM,
    *,
    include_args: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to cache method results with auto-generated keys.

    Args:
        key_prefix: Prefix for the cache key
        timeout: Cache timeout in seconds
        include_args: Whether to include args in cache key

    Usage:
        class ArticleService:
            @cached_method("articles:search", timeout=60)
            def search(self, query: str, limit: int = 10):
                return Article.objects.search(query)[:limit]
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Build cache key
            if include_args:
                # Create hash of arguments
                key_parts = [key_prefix]

                # Add positional args (skip self)
                key_parts.extend(str(arg) for arg in args[1:])

                # Add keyword args (sorted for consistency)
                for k, v in sorted(kwargs.items()):
                    key_parts.append(f"{k}={v}")

                key_string = ":".join(key_parts)

                # Hash if too long
                if len(key_string) > 200:
                    key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
                    key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key_prefix}:{key_hash}"
                else:
                    key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key_string}"
            else:
                key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key_prefix}"

            # Try to get from cache
            cached = cache.get(key)
            if cached is not None:
                return cached

            # Call function
            result = func(*args, **kwargs)

            # Cache result (convert queryset to list)
            cache_value = list(result) if hasattr(result, "__iter__") and hasattr(result, "model") else result

            cache.set(key, cache_value, timeout)
            return result

        return wrapper

    return decorator


def cache_result(
    key: str,
    timeout: int = CacheKeys.TTL_MEDIUM,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Simple decorator to cache function result with a fixed key.

    Usage:
        @cache_result("stats:global", timeout=3600)
        def get_global_stats():
            return compute_expensive_stats()
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        full_key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key}"

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            cached = cache.get(full_key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            cache.set(full_key, result, timeout)
            return result

        return wrapper

    return decorator
