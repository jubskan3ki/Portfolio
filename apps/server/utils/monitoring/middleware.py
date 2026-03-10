"""Middleware pour collecter les metriques Prometheus."""

import time
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from .metrics import (
    EXCEPTIONS_COUNTER,
    REQUEST_DURATION,
    REQUEST_IN_PROGRESS,
    REQUESTS_TOTAL,
)


class PrometheusMetricsMiddleware:
    """Middleware pour collecter les metriques HTTP pour Prometheus.

    Collecte:
    - Nombre total de requetes par methode/endpoint/status
    - Duree des requetes par methode/endpoint
    - Requetes en cours par methode/endpoint
    - Exceptions par type/endpoint
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Traite la requete et collecte les metriques."""
        # Ne pas mesurer l'endpoint /metrics lui-meme
        if request.path == "/metrics/":
            return self.get_response(request)

        method = request.method
        endpoint = self._get_endpoint(request)

        # Increment in-progress counter
        REQUEST_IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()

        start_time = time.perf_counter()
        exception_type = None

        try:
            response = self.get_response(request)
            status = str(response.status_code)
        except Exception as e:
            exception_type = type(e).__name__
            EXCEPTIONS_COUNTER.labels(
                exception_type=exception_type,
                endpoint=endpoint,
            ).inc()
            raise
        finally:
            # Calculate duration
            duration = time.perf_counter() - start_time

            # Decrement in-progress counter
            REQUEST_IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()

            # Record metrics (only if no exception or if we have a response)
            if exception_type is None:
                REQUESTS_TOTAL.labels(
                    method=method,
                    endpoint=endpoint,
                    status=status,
                ).inc()

                REQUEST_DURATION.labels(
                    method=method,
                    endpoint=endpoint,
                ).observe(duration)

        return response

    def _get_endpoint(self, request: HttpRequest) -> str:
        """Extrait le pattern d'endpoint depuis la requete.

        Normalise les URLs dynamiques pour eviter une explosion de labels.
        Ex: /api/articles/123/ -> /api/articles/{id}/
        """
        path = request.path

        # Normalise les IDs numeriques
        import re

        path = re.sub(r"/\d+/", "/{id}/", path)
        path = re.sub(r"/\d+$", "/{id}", path)

        # Normalise les UUIDs
        uuid_pattern = r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/"
        path = re.sub(uuid_pattern, "/{uuid}/", path, flags=re.IGNORECASE)

        # Normalise les slugs (si dans un pattern connu)
        # Ex: /api/articles/mon-article/ -> /api/articles/{slug}/
        known_slug_patterns = [
            r"/api/articles/[^/]+/$",
            r"/api/projects/[^/]+/$",
            r"/api/stacks/[^/]+/$",
        ]
        for pattern in known_slug_patterns:
            if re.match(pattern, path):
                path = re.sub(r"/[^/]+/$", "/{slug}/", path)
                break

        return path
