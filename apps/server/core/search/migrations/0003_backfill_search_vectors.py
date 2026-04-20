"""Backfill search_vector pour les lignes existantes."""

from django.contrib.postgres.search import SearchVector
from django.db import migrations

BACKFILL_SPEC = [
    ("articles", "Article", [("title", "A"), ("excerpt", "B")]),
    ("projects", "Project", [("title", "A"), ("description", "B"), ("long_description", "C")]),
    ("stacks", "Stack", [("name", "A"), ("description", "B"), ("content", "C")]),
    ("experiences", "Experience", [("title", "A"), ("company", "B"), ("description", "C")]),
]


def _combined_vector(fields: list[tuple[str, str]]):
    combined = None
    for field, weight in fields:
        part = SearchVector(field, weight=weight, config="french_unaccent")
        combined = part if combined is None else combined + part
    return combined


def backfill_forward(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for app_label, model_name, fields in BACKFILL_SPEC:
        model = apps.get_model(app_label, model_name)
        model.objects.update(search_vector=_combined_vector(fields))


def backfill_reverse(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for app_label, model_name, _fields in BACKFILL_SPEC:
        model = apps.get_model(app_label, model_name)
        model.objects.update(search_vector=None)


class Migration(migrations.Migration):
    dependencies = [
        ("search", "0002_install_triggers"),
    ]

    operations = [
        migrations.RunPython(backfill_forward, backfill_reverse),
    ]
