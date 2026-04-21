"""Triggers plpgsql qui maintiennent search_vector a jour (INSERT/UPDATE).

Chaque table a une fonction et un trigger dedies qui calculent le tsvector
avec des poids A/B/C selon le type de champ (titre > secondaire > tertiaire).
Couvre bulk_create / bulk_update / raw SQL | zero risque d'out-of-sync.
"""

from django.db import migrations

TRIGGERS = {
    "article": {
        "table": "articles",
        "function": "article_search_vector_update",
        "trigger": "article_search_vector_trigger",
        "body": """
            NEW.search_vector :=
                setweight(to_tsvector('french_unaccent', coalesce(NEW.title, '')), 'A') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.excerpt, '')), 'B');
        """,
        "watched_cols": "title, excerpt",
    },
    "project": {
        "table": "projects",
        "function": "project_search_vector_update",
        "trigger": "project_search_vector_trigger",
        "body": """
            NEW.search_vector :=
                setweight(to_tsvector('french_unaccent', coalesce(NEW.title, '')), 'A') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.description, '')), 'B') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.long_description, '')), 'C');
        """,
        "watched_cols": "title, description, long_description",
    },
    "stack": {
        "table": "stacks",
        "function": "stack_search_vector_update",
        "trigger": "stack_search_vector_trigger",
        "body": """
            NEW.search_vector :=
                setweight(to_tsvector('french_unaccent', coalesce(NEW.name, '')), 'A') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.description, '')), 'B') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.content, '')), 'C');
        """,
        "watched_cols": "name, description, content",
    },
    "experience": {
        "table": "experiences",
        "function": "experience_search_vector_update",
        "trigger": "experience_search_vector_trigger",
        "body": """
            NEW.search_vector :=
                setweight(to_tsvector('french_unaccent', coalesce(NEW.title, '')), 'A') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.company, '')), 'B') ||
                setweight(to_tsvector('french_unaccent', coalesce(NEW.description, '')), 'C');
        """,
        "watched_cols": "title, company, description",
    },
}


def _create_function_sql(spec: dict) -> str:
    return f"""
CREATE OR REPLACE FUNCTION {spec["function"]}() RETURNS trigger AS $$
BEGIN
    {spec["body"]}
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""


def _create_trigger_sql(spec: dict) -> str:
    return f"""
CREATE TRIGGER {spec["trigger"]}
BEFORE INSERT OR UPDATE OF {spec["watched_cols"]} ON {spec["table"]}
FOR EACH ROW EXECUTE FUNCTION {spec["function"]}();
"""


def _drop_trigger_sql(spec: dict) -> str:
    return (
        f"DROP TRIGGER IF EXISTS {spec['trigger']} ON {spec['table']};\n"
        f"DROP FUNCTION IF EXISTS {spec['function']}();"
    )


def install_triggers(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor != "postgresql":
        return
    for spec in TRIGGERS.values():
        schema_editor.execute(_create_function_sql(spec))
        schema_editor.execute(_create_trigger_sql(spec))


def uninstall_triggers(apps, schema_editor):
    del apps
    if schema_editor.connection.vendor != "postgresql":
        return
    for spec in TRIGGERS.values():
        schema_editor.execute(_drop_trigger_sql(spec))


class Migration(migrations.Migration):
    dependencies = [
        ("search", "0001_enable_extensions_and_config"),
        ("articles", "0006_article_search_vector"),
        ("projects", "0004_project_search_vector"),
        ("stacks", "0005_stack_search_vector"),
        ("experiences", "0003_experience_search_vector"),
    ]

    operations = [
        migrations.RunPython(install_triggers, uninstall_triggers),
    ]
