"""Active TimescaleDB et convertit web_vital_events / view_logs en hypertables.

Policies (aggressives) :
- web_vital_events : chunk 1j, compress > 3j (segmentby metric_name), drop > 30j
- view_logs        : chunk 7j, compress > 30j (segmentby content_type), drop > 365j
"""

from django.db import migrations

CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS timescaledb;"

WEB_VITAL_FORWARD = """
-- TimescaleDB requires the partition column to be part of every UNIQUE
-- constraint (including the PK). Recreate the PK as composite (id, created_at).
ALTER TABLE web_vital_events DROP CONSTRAINT IF EXISTS web_vital_events_pkey;
ALTER TABLE web_vital_events ADD CONSTRAINT web_vital_events_pkey PRIMARY KEY (id, created_at);
SELECT create_hypertable(
    'web_vital_events',
    'created_at',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE,
    migrate_data => TRUE
);
ALTER TABLE web_vital_events SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'metric_name',
    timescaledb.compress_orderby = 'created_at DESC'
);
SELECT add_compression_policy('web_vital_events', INTERVAL '3 days', if_not_exists => TRUE);
SELECT add_retention_policy('web_vital_events', INTERVAL '30 days', if_not_exists => TRUE);
"""

WEB_VITAL_REVERSE = """
SELECT remove_retention_policy('web_vital_events', if_exists => TRUE);
SELECT remove_compression_policy('web_vital_events', if_exists => TRUE);
ALTER TABLE web_vital_events DROP CONSTRAINT IF EXISTS web_vital_events_pkey;
ALTER TABLE web_vital_events ADD CONSTRAINT web_vital_events_pkey PRIMARY KEY (id);
"""

VIEW_LOG_FORWARD = """
-- TimescaleDB requires the partition column to be part of every UNIQUE
-- constraint (including the PK). Recreate the PK as composite (id, viewed_at).
ALTER TABLE view_logs DROP CONSTRAINT IF EXISTS view_logs_pkey;
ALTER TABLE view_logs ADD CONSTRAINT view_logs_pkey PRIMARY KEY (id, viewed_at);
SELECT create_hypertable(
    'view_logs',
    'viewed_at',
    chunk_time_interval => INTERVAL '7 days',
    if_not_exists => TRUE,
    migrate_data => TRUE
);
ALTER TABLE view_logs SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'content_type',
    timescaledb.compress_orderby = 'viewed_at DESC'
);
SELECT add_compression_policy('view_logs', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_retention_policy('view_logs', INTERVAL '365 days', if_not_exists => TRUE);
"""

VIEW_LOG_REVERSE = """
SELECT remove_retention_policy('view_logs', if_exists => TRUE);
SELECT remove_compression_policy('view_logs', if_exists => TRUE);
ALTER TABLE view_logs DROP CONSTRAINT IF EXISTS view_logs_pkey;
ALTER TABLE view_logs ADD CONSTRAINT view_logs_pkey PRIMARY KEY (id);
"""


class Migration(migrations.Migration):
    # create_hypertable + add_*_policy ne sont pas garantis transactionnels selon la version
    # de l'extension : on désactive l'atomicité Django pour éviter les rollbacks partiels.
    atomic = False

    dependencies = [
        (
            "stats",
            "0002_rename_view_logs_viewed__5b8ec5_idx_view_logs_viewed__991027_idx_and_more",
        ),
    ]

    operations = [
        migrations.RunSQL(sql=CREATE_EXTENSION, reverse_sql=migrations.RunSQL.noop),
        migrations.RunSQL(sql=WEB_VITAL_FORWARD, reverse_sql=WEB_VITAL_REVERSE),
        migrations.RunSQL(sql=VIEW_LOG_FORWARD, reverse_sql=VIEW_LOG_REVERSE),
    ]
