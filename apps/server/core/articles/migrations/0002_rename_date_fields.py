# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="Article",
            old_name="created_date",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="Article",
            old_name="updated_date",
            new_name="updated_at",
        ),
    ]
