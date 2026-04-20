"""Ajoute la colonne tsvector persistee + index GIN sur Project."""

import django.contrib.postgres.search
from django.db import migrations


def create_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(
            "CREATE INDEX IF NOT EXISTS project_search_vector_gin " "ON projects USING GIN (search_vector);"
        )


def drop_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("DROP INDEX IF EXISTS project_search_vector_gin;")


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_project_meta_description_project_seo_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
        migrations.RunPython(create_gin_index, drop_gin_index),
    ]
