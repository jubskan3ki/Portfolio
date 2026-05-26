"""Convertit audit_logs en hypertable TimescaleDB.

Policies (aggressives) :
- chunk 1j, compress > 3j (segmentby action), drop > 90j
"""

from django.db import migrations

AUDIT_FORWARD = """
CREATE EXTENSION IF NOT EXISTS timescaledb;
-- TimescaleDB requires the partition column to be part of every UNIQUE
-- constraint (including the PK). Recreate the PK as composite (id, timestamp).
ALTER TABLE audit_logs DROP CONSTRAINT IF EXISTS audit_logs_pkey;
ALTER TABLE audit_logs ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id, "timestamp");
SELECT create_hypertable(
    'audit_logs',
    'timestamp',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE,
    migrate_data => TRUE
);
ALTER TABLE audit_logs SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'action',
    timescaledb.compress_orderby = 'timestamp DESC'
);
SELECT add_compression_policy('audit_logs', INTERVAL '3 days', if_not_exists => TRUE);
SELECT add_retention_policy('audit_logs', INTERVAL '90 days', if_not_exists => TRUE);
"""

AUDIT_REVERSE = """
SELECT remove_retention_policy('audit_logs', if_exists => TRUE);
SELECT remove_compression_policy('audit_logs', if_exists => TRUE);
ALTER TABLE audit_logs DROP CONSTRAINT IF EXISTS audit_logs_pkey;
ALTER TABLE audit_logs ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);
"""


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("audit", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(sql=AUDIT_FORWARD, reverse_sql=AUDIT_REVERSE),
    ]
