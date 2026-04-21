from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_alter_user_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="twitter",
        ),
    ]
