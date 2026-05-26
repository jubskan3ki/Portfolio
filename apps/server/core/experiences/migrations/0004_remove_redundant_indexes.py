"""Remove redundant indexes already covered by FK auto-index.

- experiences_type_id_912a46_idx -> couvert par experiences_type_id_a3c0547f (FK auto)
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("experiences", "0003_experience_search_vector"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="experience",
            name="experiences_type_id_912a46_idx",
        ),
    ]
