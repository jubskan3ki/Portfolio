"""Public status page backend — aggregates Prometheus + Alertmanager state.

Exposed at GET /api/public/status/. Cached 60s to avoid hammering Prometheus
on every page load (the Nuxt /status page hits this endpoint).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, wait
from typing import Any

import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView

PROMETHEUS_URL = getattr(settings, "PROMETHEUS_INTERNAL_URL", "http://prometheus:9090")
ALERTMANAGER_URL = getattr(settings, "ALERTMANAGER_URL", "http://alertmanager:9093")
HTTP_TIMEOUT_SECONDS = 1
QUERY_WALL_TIMEOUT_SECONDS = 2.0

_QUERY_POOL = ThreadPoolExecutor(max_workers=8, thread_name_prefix="status-query")


def _prom_query_raw(query: str) -> float | None:
    """Single Prometheus query. Runs in a worker thread (see _prom_batch)."""
    try:
        resp = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=HTTP_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        data = resp.json().get("data", {}).get("result", [])
        if not data:
            return None
        return float(data[0]["value"][1])
    except (requests.RequestException, ValueError, IndexError, KeyError, TypeError):
        return None


def _prom_batch(queries: dict[str, str]) -> dict[str, float | None]:
    """Submit all queries concurrently; globally timeout at 2s wall-time.
    `wait()` uses ONE budget for all futures, unlike N*`result(timeout)` which
    would serialize and cost N*2s. Timed-out futures resolve to None; their
    threads keep running in the pool until naturally completing.
    """
    future_to_key = {_QUERY_POOL.submit(_prom_query_raw, q): key for key, q in queries.items()}
    done, not_done = wait(future_to_key.keys(), timeout=QUERY_WALL_TIMEOUT_SECONDS)
    results: dict[str, float | None] = {}
    for future in done:
        key = future_to_key[future]
        try:
            results[key] = future.result()
        except (requests.RequestException, ValueError, TypeError, IndexError, KeyError):
            # Network/parse errors from Prometheus are downgraded to None (service unknown).
            results[key] = None
    for future in not_done:
        results[future_to_key[future]] = None
    return results


def _service_status(availability: float | None) -> str:
    """Classify availability into green/amber/red."""
    if availability is None:
        return "unknown"
    if availability >= 0.999:
        return "green"
    if availability >= 0.995:
        return "amber"
    return "red"


def _fetch_incidents() -> list[dict[str, Any]]:
    """Fetch recent resolved alerts from Alertmanager (single future, same budget)."""
    future = _QUERY_POOL.submit(
        requests.get,
        f"{ALERTMANAGER_URL}/api/v2/alerts",
        params={"active": "false", "silenced": "false", "inhibited": "false"},
        timeout=HTTP_TIMEOUT_SECONDS,
    )
    done, _ = wait([future], timeout=QUERY_WALL_TIMEOUT_SECONDS)
    if future not in done:
        return []
    try:
        resp = future.result()
        resp.raise_for_status()
        alerts = resp.json()
        return [
            {
                "name": a.get("labels", {}).get("alertname", "unknown"),
                "severity": a.get("labels", {}).get("severity", "unknown"),
                "started_at": a.get("startsAt"),
                "ended_at": a.get("endsAt"),
            }
            for a in alerts[:10]
        ]
    except (requests.RequestException, ValueError, TypeError):
        return []


class StatusView(APIView):
    """Read-only public endpoint. Cached 60s."""

    permission_classes: list = []
    authentication_classes: list = []

    @method_decorator(cache_page(60))
    def get(self, _request):
        """Aggregate Prometheus SLO + Alertmanager incidents for the public status page."""
        query_map = {
            "availability_1d": "slo:api_availability:ratio_rate1d",
            "availability_3d": "slo:api_availability:ratio_rate3d",
            "latency_p95": "slo:api_latency:p95_5m",
            "api_up": 'up{job="django"}',
            "web_up": 'up{job="traefik"}',
            "db_up": 'up{job="prometheus"}',
        }
        results = _prom_batch(query_map)
        availability_1d = results["availability_1d"]
        availability_3d = results["availability_3d"]
        latency_p95 = results["latency_p95"]
        api_up = results["api_up"]
        web_up = results["web_up"]
        db_up = results["db_up"]

        uptime_30d = round(availability_3d * 100, 3) if availability_3d is not None else None
        uptime_1d = round(availability_1d * 100, 3) if availability_1d is not None else None
        latency_p95_s = round(latency_p95, 3) if latency_p95 is not None else None
        payload = {
            "uptime_30d_pct": uptime_30d,
            "uptime_1d_pct": uptime_1d,
            "latency_p95_seconds": latency_p95_s,
            "services": [
                {
                    "name": "API",
                    "status": _service_status(availability_1d) if api_up else "red",
                    "up": bool(api_up),
                },
                {
                    "name": "Web",
                    "status": "green" if web_up else "red",
                    "up": bool(web_up),
                },
                {
                    "name": "DB",
                    "status": "green" if db_up else "red",
                    "up": bool(db_up),
                },
            ],
            "incidents": _fetch_incidents(),
            "slo_targets": {
                "availability": 0.995,
                "latency_p95_seconds": 0.3,
            },
        }
        return Response(payload, status=http_status.HTTP_200_OK)
