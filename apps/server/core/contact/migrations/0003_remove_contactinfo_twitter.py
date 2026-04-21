from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0002_remove_contact_contact_status_c674f7_idx_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contactinfo",
            name="twitter",
        ),
    ]
