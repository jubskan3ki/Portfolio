"""Remove redundant indexes already covered by FK auto-index or UNIQUE constraint.

- stacks_slug_08c7f8_idx       -> couvert par stacks_slug_key (UNIQUE)
- stacks_categor_7d04ec_idx    -> couvert par stacks_category_id_f3e7af6a (FK auto)
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stacks", "0005_stack_search_vector"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="stack",
            name="stacks_slug_08c7f8_idx",
        ),
        migrations.RemoveIndex(
            model_name="stack",
            name="stacks_categor_7d04ec_idx",
        ),
    ]
