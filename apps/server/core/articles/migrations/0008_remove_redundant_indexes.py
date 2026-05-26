"""Remove redundant indexes already covered by FK auto-index or UNIQUE constraint.

- articles_slug_c8b0c2_idx       -> couvert par articles_slug_key (UNIQUE)
- articles_categor_11f3b8_idx    -> couvert par articles_category_id_8d549191 (FK auto)
- articles_is_publ_badb53_idx    -> couvert par articles_is_publ_15e299_idx (composite plus large)
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0007_article_soft_delete"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="article",
            name="articles_slug_c8b0c2_idx",
        ),
        migrations.RemoveIndex(
            model_name="article",
            name="articles_categor_11f3b8_idx",
        ),
        migrations.RemoveIndex(
            model_name="article",
            name="articles_is_publ_badb53_idx",
        ),
    ]
