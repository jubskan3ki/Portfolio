"""Remove redundant indexes already covered by FK auto-index or UNIQUE constraint.

Project:
- projects_slug_25ccba_idx       -> couvert par projects_slug_key (UNIQUE)
- projects_categor_c363bc_idx    -> couvert par projects_category_id_2110ba9e (FK auto)
- projects_status__418086_idx    -> couvert par projects_status_id_9002ad48 (FK auto)

ProjectCategory:
- project_cat_slug_8c8c80_idx    -> couvert par project_categories_slug_key (UNIQUE)
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0004_project_search_vector"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="project",
            name="projects_slug_25ccba_idx",
        ),
        migrations.RemoveIndex(
            model_name="project",
            name="projects_categor_c363bc_idx",
        ),
        migrations.RemoveIndex(
            model_name="project",
            name="projects_status__418086_idx",
        ),
        migrations.RemoveIndex(
            model_name="projectcategory",
            name="project_cat_slug_8c8c80_idx",
        ),
    ]
