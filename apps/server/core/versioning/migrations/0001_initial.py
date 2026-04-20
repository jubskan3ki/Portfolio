"""Initial migration : modele Version."""

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Version",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content_type", models.CharField(db_index=True, help_text="model_name de l'objet", max_length=100)),
                ("object_id", models.CharField(db_index=True, max_length=100)),
                ("version_number", models.PositiveIntegerField()),
                (
                    "snapshot",
                    models.JSONField(default=dict, help_text="Etat complet de l'objet au moment de cette version"),
                ),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "versioning_versions",
                "ordering": ["-version_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="version",
            constraint=models.UniqueConstraint(
                fields=("content_type", "object_id", "version_number"),
                name="unique_version_per_object",
            ),
        ),
        migrations.AddIndex(
            model_name="version",
            index=models.Index(
                fields=["content_type", "object_id", "-version_number"],
                name="versioning__content_ebb9f1_idx",
            ),
        ),
    ]
