"""Configuration de l'application versioning."""

import sys

from django.apps import AppConfig


class VersioningConfig(AppConfig):
    """App versioning : soft-delete + snapshots."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.versioning"
    verbose_name = "Versioning"

    def ready(self) -> None:
        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return
        from core.versioning import signals  # noqa: F401
