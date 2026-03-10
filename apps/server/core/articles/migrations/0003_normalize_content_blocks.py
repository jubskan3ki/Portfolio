"""Data migration: normalize article content from string[] to structured blocks."""

from django.db import migrations


def normalize_content_blocks(apps, schema_editor):
    """Convert legacy content formats to structured content blocks.

    Handles:
    - string items -> {"type": "paragraph", "content": string}
    - {"type": "text", ...} -> {"type": "paragraph", ...}
    - Already valid blocks are kept as-is
    """
    Article = apps.get_model("articles", "Article")
    articles_to_update = []

    for article in Article.objects.all():
        content = article.content
        if not isinstance(content, list):
            article.content = []
            articles_to_update.append(article)
            continue

        normalized = []
        changed = False
        for item in content:
            if isinstance(item, str):
                normalized.append({"type": "paragraph", "content": item})
                changed = True
            elif isinstance(item, dict):
                if item.get("type") == "text":
                    normalized.append({**item, "type": "paragraph"})
                    changed = True
                else:
                    normalized.append(item)
            # Skip non-string, non-dict items

        if changed:
            article.content = normalized
            articles_to_update.append(article)

    if articles_to_update:
        Article.objects.bulk_update(articles_to_update, ["content"])


def reverse_normalize(apps, schema_editor):
    """Reverse: convert paragraph blocks back to plain strings."""
    Article = apps.get_model("articles", "Article")
    articles_to_update = []

    for article in Article.objects.all():
        content = article.content
        if not isinstance(content, list):
            continue

        reversed_content = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "paragraph":
                reversed_content.append(item.get("content", ""))
            else:
                reversed_content.append(item)

        article.content = reversed_content
        articles_to_update.append(article)

    if articles_to_update:
        Article.objects.bulk_update(articles_to_update, ["content"])


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_rename_date_fields"),
    ]

    operations = [
        migrations.RunPython(normalize_content_blocks, reverse_normalize),
    ]
