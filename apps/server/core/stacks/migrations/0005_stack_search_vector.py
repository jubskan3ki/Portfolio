"""Ajoute la colonne tsvector persistee + index GIN sur Stack."""

import django.contrib.postgres.search
from django.db import migrations


def create_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(
            "CREATE INDEX IF NOT EXISTS stack_search_vector_gin " "ON stacks USING GIN (search_vector);"
        )


def drop_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("DROP INDEX IF EXISTS stack_search_vector_gin;")


class Migration(migrations.Migration):
    dependencies = [
        ("stacks", "0004_stack_meta_description_stack_seo_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="stack",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
        migrations.RunPython(create_gin_index, drop_gin_index),
    ]
