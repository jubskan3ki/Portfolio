"""Middleware d'analyse des performances DB (dev/debug uniquement).

- Compte les queries executees sur la requete courante.
- Mesure le temps cumule en DB.
- Detecte les patterns N+1 (meme SQL repete plus de N_PLUS_ONE_THRESHOLD fois).
- Expose des headers X-Query-Count, X-Query-Time et, si detecte, X-N-Plus-One.
- Log un warning pour les requetes "suspectes" (>SLOW_QUERY_MS ou >HIGH_QUERY_COUNT).
"""

from __future__ import annotations

import logging
import re
import time
from collections import Counter
from collections.abc import Callable

from django.db import connection
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("django.request")

SLOW_QUERY_MS = 500
HIGH_QUERY_COUNT = 30
N_PLUS_ONE_THRESHOLD = 5

_PARAM_PATTERN = re.compile(r"('[^']*'|\b\d+\b)")


def _fingerprint(sql: str) -> str:
    """Normalise une query SQL pour comparer des patterns (retire les litteraux)."""
    return _PARAM_PATTERN.sub("?", sql).strip().lower()


class QueryStatsMiddleware:
    """Compte + analyse les queries DB par requete.

    Actif uniquement quand `DEBUG=True` cote settings. En prod le middleware
    passe en no-op pour ne pas impacter les performances.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        from django.conf import settings

        if not getattr(settings, "DEBUG", False):
            return self.get_response(request)

        initial_queries = len(connection.queries)
        start = time.perf_counter()

        response = self.get_response(request)

        duration_ms = int((time.perf_counter() - start) * 1000)
        query_slice = connection.queries[initial_queries:]
        query_count = len(query_slice)
        query_time_ms = sum(float(q.get("time", 0)) for q in query_slice) * 1000

        response["X-Query-Count"] = str(query_count)
        response["X-Query-Time-Ms"] = f"{query_time_ms:.1f}"

        n_plus_one = self._detect_n_plus_one(query_slice)
        if n_plus_one:
            response["X-N-Plus-One"] = str(len(n_plus_one))

        self._log_if_suspicious(request, query_count, duration_ms, n_plus_one)
        return response

    @staticmethod
    def _detect_n_plus_one(queries: list[dict]) -> list[tuple[str, int]]:
        """Retourne les patterns SQL repetes > N_PLUS_ONE_THRESHOLD fois."""
        counter: Counter[str] = Counter()
        for q in queries:
            sql = q.get("sql", "")
            if not sql:
                continue
            counter[_fingerprint(sql)] += 1
        return [(sql, n) for sql, n in counter.items() if n > N_PLUS_ONE_THRESHOLD]

    @staticmethod
    def _log_if_suspicious(
        request: HttpRequest,
        query_count: int,
        duration_ms: int,
        n_plus_one: list[tuple[str, int]],
    ) -> None:
        if query_count > HIGH_QUERY_COUNT or duration_ms > SLOW_QUERY_MS or n_plus_one:
            logger.warning(
                "Perf alert: %s %s -> %d queries, %dms%s",
                request.method,
                request.path,
                query_count,
                duration_ms,
                f", N+1 patterns: {len(n_plus_one)}" if n_plus_one else "",
            )
