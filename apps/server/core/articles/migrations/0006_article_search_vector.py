"""Ajoute la colonne tsvector persistee + index GIN sur Article."""

import django.contrib.postgres.search
from django.db import migrations


def create_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(
            "CREATE INDEX IF NOT EXISTS article_search_vector_gin " "ON articles USING GIN (search_vector);"
        )


def drop_gin_index(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("DROP INDEX IF EXISTS article_search_vector_gin;")


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0005_article_meta_description_article_seo_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
        migrations.RunPython(create_gin_index, drop_gin_index),
    ]
