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
    """Cache queryset; cache_key peut etre callable(args)."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if callable(cache_key):
                try:
                    key = cache_key(*args[1:], **kwargs)  # skip self
                except TypeError:
                    key = cache_key(**kwargs)
            else:
                key = cache_key

            cached = cache.get(key)
            if cached is not None:
                logger.debug("Cache hit: %s", key)
                return cached

            logger.debug("Cache miss: %s", key)
            result = func(*args, **kwargs)

            if serializer and result is not None:
                try:
                    cache_value = serializer(result)
                except Exception as e:
                    logger.warning("Failed to serialize for cache: %s", e)
                    return result
            else:
                # queryset -> list pour serialisation
                cache_value = list(result) if hasattr(result, "__iter__") and hasattr(result, "model") else result

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
    """Cache methode; cle auto-generee depuis args."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if include_args:
                key_parts = [key_prefix]
                key_parts.extend(str(arg) for arg in args[1:])  # skip self
                for k, v in sorted(kwargs.items()):
                    key_parts.append(f"{k}={v}")

                key_string = ":".join(key_parts)

                # Hash si cle > 200 chars
                if len(key_string) > 200:
                    key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
                    key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key_prefix}:{key_hash}"
                else:
                    key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key_string}"
            else:
                key = f"{CacheKeys.PREFIX}:{CacheKeys.VERSION}:{key_prefix}"

            cached = cache.get(key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)

            cache_value = list(result) if hasattr(result, "__iter__") and hasattr(result, "model") else result

            cache.set(key, cache_value, timeout)
            return result

        return wrapper

    return decorator


def cache_result(
    key: str,
    timeout: int = CacheKeys.TTL_MEDIUM,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Cache resultat fonction avec cle fixe."""

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
