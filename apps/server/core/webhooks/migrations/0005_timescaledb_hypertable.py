"""Convertit webhook_deliveries en hypertable TimescaleDB.

Policies (aggressives) :
- chunk 1j, compress > 7j (segmentby webhook_id), drop > 30j

La UniqueConstraint(webhook, event_id) est retiree (incompatible avec une hypertable
partitionnee sur created_at) ; la deduplication est garantie applicativement via un
pg_advisory_xact_lock dans WebhookDispatcher.
"""

from django.db import migrations, models

WEBHOOK_FORWARD = """
CREATE EXTENSION IF NOT EXISTS timescaledb;
ALTER TABLE webhook_deliveries DROP CONSTRAINT IF EXISTS unique_webhook_event_id;
CREATE INDEX IF NOT EXISTS webhook_dedup_lookup_idx ON webhook_deliveries (webhook_id, event_id);
ALTER TABLE webhook_deliveries DROP CONSTRAINT IF EXISTS webhook_deliveries_pkey;
ALTER TABLE webhook_deliveries ADD CONSTRAINT webhook_deliveries_pkey PRIMARY KEY (id, created_at);
SELECT create_hypertable(
    'webhook_deliveries',
    'created_at',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE,
    migrate_data => TRUE
);
ALTER TABLE webhook_deliveries SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'webhook_id',
    timescaledb.compress_orderby = 'created_at DESC'
);
SELECT add_compression_policy('webhook_deliveries', INTERVAL '7 days', if_not_exists => TRUE);
SELECT add_retention_policy('webhook_deliveries', INTERVAL '30 days', if_not_exists => TRUE);
"""

WEBHOOK_REVERSE = """
SELECT remove_retention_policy('webhook_deliveries', if_exists => TRUE);
SELECT remove_compression_policy('webhook_deliveries', if_exists => TRUE);
ALTER TABLE webhook_deliveries DROP CONSTRAINT IF EXISTS webhook_deliveries_pkey;
ALTER TABLE webhook_deliveries ADD CONSTRAINT webhook_deliveries_pkey PRIMARY KEY (id);
DROP INDEX IF EXISTS webhook_dedup_lookup_idx;
ALTER TABLE webhook_deliveries ADD CONSTRAINT unique_webhook_event_id UNIQUE (webhook_id, event_id);
"""


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("webhooks", "0004_webhook_webhooks_is_acti_6b7670_idx_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveConstraint(
                    model_name="webhookdelivery",
                    name="unique_webhook_event_id",
                ),
                migrations.AddIndex(
                    model_name="webhookdelivery",
                    index=models.Index(
                        fields=["webhook", "event_id"],
                        name="webhook_dedup_lookup_idx",
                    ),
                ),
            ],
            database_operations=[],
        ),
        migrations.RunSQL(sql=WEBHOOK_FORWARD, reverse_sql=WEBHOOK_REVERSE),
    ]
