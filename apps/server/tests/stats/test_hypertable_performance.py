"""E2E TimescaleDB : extension chargée, web_vital_events est une hypertable,
et une agrégation sur 10k rows tourne sous 100ms.

Si ce test échoue avec "extension not installed", c'est que la DB de test n'a pas
l'image timescale/timescaledb (cf. .gitlab-ci.yml et docker-compose.yml).
"""

from __future__ import annotations

import time

import pytest
from django.db import connection

HYPERTABLE = "web_vital_events"
ROW_COUNT = 10_000
QUERY_BUDGET_MS = 100.0


@pytest.mark.django_db(transaction=True)
def test_timescaledb_extension_loaded() -> None:
    with connection.cursor() as cur:
        cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';")
        row = cur.fetchone()
    assert row is not None, "TimescaleDB extension not installed on the test database"


@pytest.mark.django_db(transaction=True)
def test_web_vital_events_is_hypertable() -> None:
    with connection.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM timescaledb_information.hypertables " "WHERE hypertable_name = %s",
            [HYPERTABLE],
        )
        row = cur.fetchone()
    assert row is not None, f"{HYPERTABLE} is not registered as a hypertable"


@pytest.mark.django_db(transaction=True)
def test_aggregation_on_10k_rows_under_budget() -> None:
    # Ingestion via generate_series : ~10k rows répartis sur 7 jours.
    # Beaucoup plus rapide que bulk_create + UPDATE croisant les chunks.
    with connection.cursor() as cur:
        cur.execute(
            """
            INSERT INTO web_vital_events (
                metric_name, value, rating, delta, metric_id, path,
                full_url, user_agent, language, viewport_width, viewport_height,
                connection_type, is_mobile, created_at
            )
            SELECT
                (ARRAY['LCP','CLS','INP','FCP','TTFB'])[1 + (g %% 5)],
                100.0 + (g %% 1000),
                (ARRAY['good','needs-improvement','poor'])[1 + (g %% 3)],
                0,
                'id-' || g::text,
                (ARRAY['/','/blog','/projects','/stacks','/contact'])[1 + (g %% 5)],
                '',
                'test',
                NULL, NULL, NULL, NULL, NULL,
                NOW() - (g * INTERVAL '60 seconds')
            FROM generate_series(1, %s) g
            """,
            [ROW_COUNT],
        )
        cur.execute(f"ANALYZE {HYPERTABLE};")

    # Plusieurs chunks doivent exister (sinon le test n'évalue pas TimescaleDB).
    with connection.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM timescaledb_information.chunks " "WHERE hypertable_name = %s",
            [HYPERTABLE],
        )
        chunk_count = cur.fetchone()[0]
    assert chunk_count >= 2, f"expected >= 2 chunks, got {chunk_count}"

    # Query agrégée : p75 par métrique sur la fenêtre 7j.
    query = """
        SELECT
            metric_name,
            percentile_cont(0.75) WITHIN GROUP (ORDER BY value) AS p75,
            count(*) AS samples
        FROM web_vital_events
        WHERE created_at >= NOW() - INTERVAL '7 days'
        GROUP BY metric_name
        ORDER BY metric_name
    """
    start = time.perf_counter()
    with connection.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert len(rows) == 5, f"expected 5 metrics, got {len(rows)}"
    assert elapsed_ms < QUERY_BUDGET_MS, (
        f"aggregation took {elapsed_ms:.1f}ms, budget {QUERY_BUDGET_MS}ms " f"(chunks={chunk_count}, rows={ROW_COUNT})"
    )
