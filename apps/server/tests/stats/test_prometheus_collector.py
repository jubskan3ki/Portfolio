"""Tests pour le custom Prometheus collector Web Vitals."""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.utils import timezone

from core.stats.models import WebVitalEvent
from core.stats.prometheus import WebVitalsCollector


def _make_event(metric: str, value: float, rating: str, age_minutes: int = 0) -> WebVitalEvent:
    event = WebVitalEvent.objects.create(
        metric_name=metric,
        value=value,
        rating=rating,
        delta=0,
        metric_id=f"{metric}-{value}",
        path="/",
        full_url="https://example.com/",
        user_agent="UA",
    )
    if age_minutes:
        WebVitalEvent.objects.filter(pk=event.pk).update(created_at=timezone.now() - timedelta(minutes=age_minutes))
    return event


def _index_samples(metric_families: list) -> dict[str, dict[tuple[tuple[str, str], ...], float]]:
    """Reduce collector output to a {family_name: {labels_tuple: value}} dict."""
    result: dict[str, dict[tuple[tuple[str, str], ...], float]] = {}
    for family in metric_families:
        bucket = result.setdefault(family.name, {})
        for sample in family.samples:
            label_key = tuple(sorted(sample.labels.items()))
            bucket[label_key] = sample.value
    return result


@pytest.mark.django_db
def test_collector_yields_percentiles_and_counts() -> None:
    for value in (1000, 1500, 2000, 2500, 3000, 4000, 5000):
        rating = "good" if value < 2500 else ("needs-improvement" if value < 4000 else "poor")
        _make_event("LCP", value, rating)

    families = list(WebVitalsCollector().collect())
    samples = _index_samples(families)

    lcp_key = (("metric", "LCP"),)
    # 7 valeurs triees, p75 = index round(6*0.75)=4 (banker), p95 = index round(6*0.95)=6
    assert samples["web_vitals_p75"][lcp_key] == 3000.0
    assert samples["web_vitals_p95"][lcp_key] == 5000.0

    assert samples["web_vitals_events"][(("metric", "LCP"), ("rating", "good"))] == 3
    assert samples["web_vitals_events"][(("metric", "LCP"), ("rating", "needs-improvement"))] == 2
    assert samples["web_vitals_events"][(("metric", "LCP"), ("rating", "poor"))] == 2


@pytest.mark.django_db
def test_collector_ignores_events_outside_window() -> None:
    _make_event("LCP", 999, "good", age_minutes=30)
    _make_event("LCP", 1200, "good")

    families = list(WebVitalsCollector().collect())
    samples = _index_samples(families)

    lcp_key = (("metric", "LCP"),)
    assert samples["web_vitals_mean"][lcp_key] == 1200.0


@pytest.mark.django_db
def test_collector_emits_no_metric_lines_when_empty() -> None:
    families = list(WebVitalsCollector().collect())
    samples = _index_samples(families)

    for family_name in ("web_vitals_p75", "web_vitals_p95", "web_vitals_mean", "web_vitals_events"):
        assert samples.get(family_name, {}) == {}
