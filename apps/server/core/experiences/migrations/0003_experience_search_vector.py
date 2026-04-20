"""Ajoute la colonne tsvector persistee + index GIN sur Experience."""

import django.contrib.postgres.search
from django.db import migrations


def create_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(
            "CREATE INDEX IF NOT EXISTS experience_search_vector_gin " "ON experiences USING GIN (search_vector);"
        )


def drop_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("DROP INDEX IF EXISTS experience_search_vector_gin;")


class Migration(migrations.Migration):
    dependencies = [
        ("experiences", "0002_alter_experience_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
        migrations.RunPython(create_gin_index, drop_gin_index),
    ]
