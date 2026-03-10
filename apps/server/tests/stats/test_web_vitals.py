"""Tests API pour l'ingestion et la synthese Web Vitals."""

from __future__ import annotations

from typing import Any

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from core.stats.models import WebVitalEvent


def _payload(**overrides: Any) -> dict[str, Any]:
    payload = {
        "name": "LCP",
        "value": 1800.5,
        "rating": "good",
        "delta": 42.3,
        "id": "v4-1234",
        "page": "/projects/demo",
        "url": "https://example.com/projects/demo",
        "userAgent": "Mozilla/5.0 test-agent",
        "language": "fr-FR",
        "viewport": {"width": 1280, "height": 720},
        "connectionType": "4g",
        "isMobile": False,
        "timestamp": "2026-03-02T18:00:00Z",
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
def test_web_vitals_ingest_valid_payload(api_client: APIClient) -> None:
    response = api_client.post("/api/stats/web-vitals/", _payload(), format="json")

    assert response.status_code == 202
    assert WebVitalEvent.objects.count() == 1
    event = WebVitalEvent.objects.first()
    assert event is not None
    assert event.metric_name == "LCP"
    assert event.path == "/projects/demo"


@pytest.mark.django_db
def test_web_vitals_ingest_invalid_metric(api_client: APIClient) -> None:
    response = api_client.post("/api/stats/web-vitals/", _payload(name="XYZ"), format="json")

    assert response.status_code == 400
    assert WebVitalEvent.objects.count() == 0


@pytest.mark.django_db
def test_web_vitals_ingest_field_too_long(api_client: APIClient) -> None:
    too_long_path = "/" + ("x" * 600)
    response = api_client.post("/api/stats/web-vitals/", _payload(page=too_long_path), format="json")

    assert response.status_code == 400
    assert WebVitalEvent.objects.count() == 0


@pytest.mark.django_db
def test_web_vitals_ingest_throttled(api_client: APIClient) -> None:
    from core.stats.throttles import WebVitalsThrottle

    cache.clear()
    # Patch THROTTLE_RATES directly (SimpleRateThrottle caches rates at class level)
    original_rate = WebVitalsThrottle.THROTTLE_RATES.get("web_vitals")
    WebVitalsThrottle.THROTTLE_RATES["web_vitals"] = "1/minute"
    try:
        first = api_client.post("/api/stats/web-vitals/", _payload(id="v4-first"), format="json")
        second = api_client.post("/api/stats/web-vitals/", _payload(id="v4-second"), format="json")

        assert first.status_code == 202
        assert second.status_code == 429
    finally:
        if original_rate is not None:
            WebVitalsThrottle.THROTTLE_RATES["web_vitals"] = original_rate
        else:
            WebVitalsThrottle.THROTTLE_RATES.pop("web_vitals", None)


@pytest.mark.django_db
def test_web_vitals_summary_requires_admin(api_client: APIClient) -> None:
    response = api_client.get("/api/stats/web-vitals/summary/?days=7")
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_web_vitals_summary_for_admin(authenticated_client: APIClient) -> None:
    WebVitalEvent.objects.create(
        metric_name="LCP",
        value=2400,
        rating="needs-improvement",
        delta=100,
        metric_id="metric-1",
        path="/",
        full_url="https://example.com/",
        user_agent="Mozilla/5.0",
    )
    WebVitalEvent.objects.create(
        metric_name="LCP",
        value=1200,
        rating="good",
        delta=50,
        metric_id="metric-2",
        path="/",
        full_url="https://example.com/",
        user_agent="Mozilla/5.0",
    )

    response = authenticated_client.get("/api/stats/web-vitals/summary/?days=7")

    assert response.status_code == 200
    data = response.json()
    assert data["window_days"] == 7
    assert data["total_events"] == 2
    assert len(data["metrics"]) == 1
    assert data["metrics"][0]["metric_name"] == "LCP"
    assert data["metrics"][0]["count"] == 2
