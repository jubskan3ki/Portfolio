"""Conditional cache middleware for API responses."""

import hashlib
import logging
import re

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("cache")

# Regex pour les caracteres invalides dans les cles memcached (espaces, controle chars)
INVALID_CACHE_KEY_CHARS = re.compile(r"[\s\x00-\x1f\x7f]")

DEFAULT_CACHEABLE_URLS = [
    "/api/projects/",
    "/api/experiences/",
    "/api/stacks/",
    "/api/articles/",
]

DEFAULT_NON_CACHEABLE_URLS = [
    "/api/contact/",
    "/api/admin/",
    "/api/users/",
]

DEFAULT_CACHE_TIMEOUT = 300
CACHE_KEY_PREFIX = "api_cache"
CACHE_KEYS_SET = "api_cache_keys"

# TTL differencies par endpoint (en secondes)
CACHE_TTL_MAP: dict[str, int] = {
    "/api/stacks/": 600,  # 10 min
    "/api/experiences/": 600,  # 10 min
    "/api/projects/": 600,  # 10 min
    "/api/articles/": 300,  # 5 min
}


class CacheInvalidator:
    """Utility class for cache invalidation."""

    # Mapping des endpoints aux patterns de cache a invalider
    INVALIDATION_MAP: dict[str, list[str]] = {
        "/api/projects/": ["/api/projects/"],
        "/api/articles/": ["/api/articles/"],
        "/api/experiences/": ["/api/experiences/"],
        "/api/stacks/": ["/api/stacks/"],
        # Transfer imports invalidate the corresponding module caches
        "/api/transfer/": [
            "/api/projects/",
            "/api/articles/",
            "/api/experiences/",
            "/api/stacks/",
        ],
    }

    @classmethod
    def invalidate_for_path(cls, path: str) -> int:
        """Invalide le cache pour un chemin donne."""
        invalidated = 0
        for pattern, targets in cls.INVALIDATION_MAP.items():
            if path.startswith(pattern):
                for target in targets:
                    count = cls._invalidate_pattern(target)
                    invalidated += count
                break
        return invalidated

    @classmethod
    def _invalidate_pattern(cls, pattern: str) -> int:
        """Invalide toutes les cles de cache correspondant a un pattern.

        Note: Utilise une approche atomique avec try/except pour gerer
        les modifications concurrentes de CACHE_KEYS_SET.
        """
        keys_to_delete: set[str] = set()

        # Recuperer les cles actuelles
        all_keys = cache.get(CACHE_KEYS_SET, set())
        if not isinstance(all_keys, set):
            all_keys = set(all_keys) if all_keys else set()

        for key in all_keys:
            if pattern in key:
                keys_to_delete.add(key)

        if keys_to_delete:
            # Supprimer les cles de cache
            cache.delete_many(list(keys_to_delete))

            # Mise a jour atomique: re-lire et recalculer
            # pour eviter les race conditions
            current_keys = cache.get(CACHE_KEYS_SET, set())
            if not isinstance(current_keys, set):
                current_keys = set(current_keys) if current_keys else set()
            remaining_keys = current_keys - keys_to_delete
            cache.set(CACHE_KEYS_SET, remaining_keys, timeout=None)

            logger.info("Cache invalide: %d cles pour pattern '%s'", len(keys_to_delete), pattern)

        return len(keys_to_delete)

    @classmethod
    def invalidate_all(cls) -> int:
        """Invalide tout le cache API."""
        all_keys = cache.get(CACHE_KEYS_SET, set())
        count = len(all_keys)
        if all_keys:
            cache.delete_many(list(all_keys))
            cache.delete(CACHE_KEYS_SET)
            logger.info("Cache API completement invalide: %d cles", count)
        return count


class ConditionalCacheMiddleware(MiddlewareMixin):
    """Cache GET responses for frequently accessed endpoints."""

    MUTATION_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.cacheable_urls = getattr(settings, "API_CACHE_URLS", DEFAULT_CACHEABLE_URLS)
        self.non_cacheable_urls = getattr(settings, "API_NON_CACHE_URLS", DEFAULT_NON_CACHEABLE_URLS)
        self.cache_timeout = getattr(settings, "API_CACHE_TIMEOUT", DEFAULT_CACHE_TIMEOUT)
        self.ttl_map = getattr(settings, "API_CACHE_TTL_MAP", CACHE_TTL_MAP)

    def _get_ttl(self, path: str) -> int:
        """Return endpoint-specific TTL, or default."""
        for prefix, ttl in self.ttl_map.items():
            if path.startswith(prefix):
                return ttl
        return self.cache_timeout

    def _is_cacheable(self, path: str) -> bool:
        """Check if path should be cached."""
        if any(path.startswith(url) for url in self.non_cacheable_urls):
            return False
        return any(path.startswith(url) for url in self.cacheable_urls)

    def _get_cache_key(self, request: HttpRequest) -> str:
        """Generate cache key from request URL.

        Sanitizes the path to remove characters invalid for memcached.
        """
        url = request.build_absolute_uri()
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:32]
        # Remplacer les caracteres invalides pour memcached par des underscores
        safe_path = INVALID_CACHE_KEY_CHARS.sub("_", request.path_info)
        return f"{CACHE_KEY_PREFIX}:{safe_path}:{url_hash}"

    def _should_cache(self, request: HttpRequest) -> bool:
        """Check if request should use cache."""
        if not getattr(settings, "API_CACHE_ENABLED", True):
            return False
        if request.method != "GET":
            return False
        if hasattr(request, "user") and request.user.is_authenticated:
            return False
        return self._is_cacheable(request.path_info)

    def _track_cache_key(self, key: str) -> None:
        """Track cache key for invalidation."""
        all_keys = cache.get(CACHE_KEYS_SET, set())
        all_keys.add(key)
        cache.set(CACHE_KEYS_SET, all_keys, timeout=None)

    def process_request(self, request: HttpRequest) -> HttpResponse | None:
        """Return cached response if available."""
        if not self._should_cache(request):
            return None

        cached = cache.get(self._get_cache_key(request))
        if cached:
            # ETag conditional: return 304 if content unchanged
            etag = cached.get("etag")
            if etag and request.META.get("HTTP_IF_NONE_MATCH") == etag:
                response = HttpResponse(status=304)
                response["ETag"] = etag
                if settings.DEBUG:
                    response["X-API-Cache"] = "hit-304"
                return response

            response = HttpResponse(
                content=cached["content"],
                content_type=cached["content_type"],
                status=cached["status_code"],
            )
            if etag:
                response["ETag"] = etag
            if settings.DEBUG:
                response["X-API-Cache"] = "hit"
            return response
        return None

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Cache successful GET responses and invalidate on mutations."""
        # Invalider le cache apres une mutation reussie
        if request.method in self.MUTATION_METHODS and 200 <= response.status_code < 300:
            invalidated = CacheInvalidator.invalidate_for_path(request.path_info)
            if invalidated > 0 and settings.DEBUG:
                response["X-API-Cache-Invalidated"] = str(invalidated)

        if not self._should_cache(request):
            return response

        if response.status_code != 200:
            return response

        if response.get("Cache-Control") == "no-store":
            return response

        if getattr(response, "no_api_cache", False):
            return response

        # Compute ETag from response content
        etag = f'"{hashlib.md5(response.content).hexdigest()}"'

        # Store rendered content with ETag
        cache_key = self._get_cache_key(request)
        cache_data = {
            "content": response.content,
            "content_type": response.get("Content-Type", "application/json"),
            "status_code": response.status_code,
            "etag": etag,
        }
        ttl = self._get_ttl(request.path_info)
        cache.set(cache_key, cache_data, ttl)
        self._track_cache_key(cache_key)

        response["ETag"] = etag

        if settings.DEBUG:
            response["X-API-Cache"] = "miss"

        return response


# Export pour utilisation externe
invalidate_cache = CacheInvalidator.invalidate_for_path
invalidate_all_cache = CacheInvalidator.invalidate_all
