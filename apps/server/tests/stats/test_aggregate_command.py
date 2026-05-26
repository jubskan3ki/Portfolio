"""Tests pour la commande management aggregate_web_vitals."""

from __future__ import annotations

import json
from datetime import timedelta
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from core.stats.models import WebVitalEvent


def _make_event(value: float, rating: str, age_days: int = 0) -> WebVitalEvent:
    # web_vital_events is a TimescaleDB hypertable: UPDATE-ing a row's created_at
    # across chunks is rejected, and auto_now_add overrides any value passed to
    # create()/bulk_create(). We INSERT directly so created_at lands in the
    # right chunk on first write.
    from django.db import connection

    target_ts = timezone.now() - timedelta(days=age_days)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO web_vital_events
                (metric_name, value, rating, delta, metric_id, path, full_url, user_agent, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            ["LCP", value, rating, 0, f"id-{value}", "/", "https://example.com/", "UA", target_ts],
        )
        event_id = cursor.fetchone()[0]
    return WebVitalEvent.objects.get(id=event_id)


@pytest.mark.django_db
def test_command_outputs_json_summary() -> None:
    _make_event(1000, "good")
    _make_event(2000, "good")
    _make_event(3000, "needs-improvement")

    out = StringIO()
    call_command("aggregate_web_vitals", "--days", "1", "--json", stdout=out)

    payload = json.loads(out.getvalue())
    assert payload["window_days"] == 1
    assert payload["total_events"] == 3
    assert payload["purged"] == 0

    metric = next(m for m in payload["metrics"] if m["metric_name"] == "LCP")
    assert metric["count"] == 3
    assert metric["ratings"]["good"] == 2
    assert metric["ratings"]["needs-improvement"] == 1
    assert metric["p75"] == 3000


@pytest.mark.django_db
def test_command_purges_old_events() -> None:
    _make_event(1000, "good")
    _make_event(2000, "good", age_days=40)
    _make_event(2500, "good", age_days=50)

    out = StringIO()
    call_command(
        "aggregate_web_vitals",
        "--days",
        "1",
        "--retention-days",
        "30",
        "--json",
        stdout=out,
    )

    payload = json.loads(out.getvalue())
    assert payload["purged"] == 2
    assert WebVitalEvent.objects.count() == 1


@pytest.mark.django_db
def test_command_rejects_invalid_args() -> None:
    with pytest.raises(CommandError):
        call_command("aggregate_web_vitals", "--days", "0")

    with pytest.raises(CommandError):
        call_command("aggregate_web_vitals", "--days", "10", "--retention-days", "5")


@pytest.mark.django_db
def test_command_text_output_handles_empty() -> None:
    out = StringIO()
    call_command("aggregate_web_vitals", "--days", "1", stdout=out)

    output = out.getvalue()
    assert "0 events" in output
    assert "aucune metrique" in output
