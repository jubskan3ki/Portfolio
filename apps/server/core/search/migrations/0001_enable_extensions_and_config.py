"""Extensions Postgres + configuration TEXT SEARCH french_unaccent."""

from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

CREATE_CONFIG_SQL = """
CREATE TEXT SEARCH CONFIGURATION french_unaccent (COPY = french);
ALTER TEXT SEARCH CONFIGURATION french_unaccent
  ALTER MAPPING FOR hword, hword_part, word
  WITH unaccent, french_stem;
"""

DROP_CONFIG_SQL = "DROP TEXT SEARCH CONFIGURATION IF EXISTS french_unaccent;"


def create_config(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(CREATE_CONFIG_SQL)


def drop_config(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(DROP_CONFIG_SQL)


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        CreateExtension("unaccent"),
        CreateExtension("pg_trgm"),
        migrations.RunPython(create_config, drop_config),
    ]
