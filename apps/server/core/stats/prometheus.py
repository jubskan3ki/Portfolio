"""Collecteur Prometheus pour exposer les Web Vitals agreges.

Strategie : pull-based custom collector qui interroge la DB a chaque scrape
sur une fenetre glissante courte. Pas de probleme multi-worker (chaque scrape
remonte des donnees identiques quel que soit le worker gunicorn qui repond).
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import timedelta

from django.utils import timezone
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.registry import Collector

logger = logging.getLogger("core.stats")

WINDOW_MINUTES = 5
RATINGS = ("good", "needs-improvement", "poor")


class WebVitalsCollector(Collector):
    """Expose les percentiles + ratings Web Vitals sur la fenetre glissante."""

    _registered: bool = False

    def collect(self) -> Iterator[GaugeMetricFamily | CounterMetricFamily]:
        from .models import WebVitalEvent
        from .services.web_vitals import WebVitalsService

        since = timezone.now() - timedelta(minutes=WINDOW_MINUTES)

        try:
            summary = WebVitalsService._summarize_queryset(WebVitalEvent.objects.filter(created_at__gte=since))
        except Exception:
            logger.exception("WebVitalsCollector: failed to query events")
            return

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

        for row in summary:
            metric_name = row["metric_name"]
            p75.add_metric([metric_name], row["p75"] or 0.0)
            p95.add_metric([metric_name], row["p95"] or 0.0)
            mean_metric.add_metric([metric_name], row["mean"] or 0.0)
            for rating in RATINGS:
                events_total.add_metric([metric_name, rating], float(row["ratings"].get(rating, 0)))

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
