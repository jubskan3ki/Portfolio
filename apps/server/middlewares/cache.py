"""Conditional cache middleware for API responses."""

import hashlib
import logging
import re
from urllib.parse import parse_qsl, urlencode

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
    def _invalidate_pattern(cls, target: str) -> int:
        """Invalide les entrees de cache d'un endpoint via delete_pattern (Redis).

        Les cles ont la forme `api_cache:<path>:<hash>`, donc le glob
        `api_cache:<path>*` couvre la liste et les details. Aucune borne a
        maintenir (plus de registre CACHE_KEYS_SET racy/non borne).
        """
        pattern = f"{CACHE_KEY_PREFIX}:{target}*"
        try:
            if hasattr(cache, "delete_pattern"):
                count = cache.delete_pattern(pattern)
                if count:
                    logger.info("Cache invalide: %d cles pour pattern '%s'", count, target)
                return count
        except Exception as e:
            logger.warning("delete_pattern failed for %s: %s", pattern, e)
            return 0

        logger.warning("Cache backend sans delete_pattern: invalidation ignoree pour %s", target)
        return 0

    @classmethod
    def invalidate_all(cls) -> int:
        """Invalide tout le cache API."""
        pattern = f"{CACHE_KEY_PREFIX}:*"
        try:
            if hasattr(cache, "delete_pattern"):
                count = cache.delete_pattern(pattern)
                logger.info("Cache API completement invalide: %d cles", count)
                return count
        except Exception as e:
            logger.warning("delete_pattern failed for %s: %s", pattern, e)
            return 0

        logger.warning("Cache backend sans delete_pattern: invalidate_all ignore")
        return 0


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
        """Generate cache key from path + normalized querystring.

        N'inclut PAS le Host (evite le cache poisoning / split via l'en-tete
        Host) et normalise l'ordre des parametres (evite des entrees dupliquees
        pour `?a=1&b=2` vs `?b=2&a=1`).
        """
        query = request.META.get("QUERY_STRING", "")
        normalized_qs = urlencode(sorted(parse_qsl(query, keep_blank_values=True))) if query else ""
        qs_hash = hashlib.sha256(normalized_qs.encode()).hexdigest()[:32]
        # Remplacer les caracteres de cle invalides par des underscores
        safe_path = INVALID_CACHE_KEY_CHARS.sub("_", request.path_info)
        return f"{CACHE_KEY_PREFIX}:{safe_path}:{qs_hash}"

    def _should_cache(self, request: HttpRequest) -> bool:
        """Check if request should use cache."""
        if not getattr(settings, "API_CACHE_ENABLED", True):
            return False
        if request.method != "GET":
            return False
        if hasattr(request, "user") and request.user.is_authenticated:
            return False
        return self._is_cacheable(request.path_info)

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
        etag = f'"{hashlib.md5(response.content, usedforsecurity=False).hexdigest()}"'

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

        response["ETag"] = etag

        if settings.DEBUG:
            response["X-API-Cache"] = "miss"

        return response


# Export pour utilisation externe
invalidate_cache = CacheInvalidator.invalidate_for_path
invalidate_all_cache = CacheInvalidator.invalidate_all
