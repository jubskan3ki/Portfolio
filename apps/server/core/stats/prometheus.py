"""Collecteur Prometheus pour exposer les Web Vitals agreges.

Strategie : pull-based custom collector qui interroge la DB a chaque scrape
sur une fenetre glissante courte. Pas de probleme multi-worker (chaque scrape
remonte des donnees identiques quel que soit le worker gunicorn qui repond).
"""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Iterator
from datetime import timedelta
from statistics import fmean

from django.utils import timezone
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.registry import Collector

logger = logging.getLogger("core.stats")

WINDOW_MINUTES = 5
RATINGS = ("good", "needs-improvement", "poor")


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = round((len(sorted_values) - 1) * (percentile / 100))
    return float(sorted_values[index])


class WebVitalsCollector(Collector):
    """Expose les percentiles + ratings Web Vitals sur la fenetre glissante."""

    _registered: bool = False

    def collect(self) -> Iterator[GaugeMetricFamily | CounterMetricFamily]:
        from .models import WebVitalEvent

        since = timezone.now() - timedelta(minutes=WINDOW_MINUTES)

        try:
            events = list(WebVitalEvent.objects.filter(created_at__gte=since).values("metric_name", "value", "rating"))
        except Exception:
            logger.exception("WebVitalsCollector: failed to query events")
            return

        values_by_metric: dict[str, list[float]] = defaultdict(list)
        ratings_count: dict[tuple[str, str], int] = defaultdict(int)

        for event in events:
            metric_name = str(event["metric_name"])
            values_by_metric[metric_name].append(float(event["value"]))
            ratings_count[(metric_name, str(event["rating"]))] += 1

        p75 = GaugeMetricFamily(
            "web_vitals_p75",
            "75th percentile of a Web Vital metric over the last 5 minutes (ms or unitless for CLS).",
            labels=["metric"],
        )
        p95 = GaugeMetricFamily(
            "web_vitals_p95",
            "95th percentile of a Web Vital metric over the last 5 minutes.",
            labels=["metric"],
        )
        mean_metric = GaugeMetricFamily(
            "web_vitals_mean",
            "Mean value of a Web Vital metric over the last 5 minutes.",
            labels=["metric"],
        )
        events_total = GaugeMetricFamily(
            "web_vitals_events",
            "Number of Web Vital events received in the last 5 minutes, by metric and rating.",
            labels=["metric", "rating"],
        )

        for metric_name, values in values_by_metric.items():
            p75.add_metric([metric_name], _percentile(values, 75))
            p95.add_metric([metric_name], _percentile(values, 95))
            mean_metric.add_metric([metric_name], float(fmean(values)) if values else 0.0)

        observed_metrics = set(values_by_metric.keys())
        for metric_name in observed_metrics:
            for rating in RATINGS:
                events_total.add_metric([metric_name, rating], float(ratings_count.get((metric_name, rating), 0)))

        yield p75
        yield p95
        yield mean_metric
        yield events_total


def register_collector() -> None:
    """Enregistre le collector dans le REGISTRY global (idempotent)."""
    if WebVitalsCollector._registered:
        return

    from prometheus_client import REGISTRY

    REGISTRY.register(WebVitalsCollector())
    WebVitalsCollector._registered = True
    logger.debug("WebVitalsCollector registered")
