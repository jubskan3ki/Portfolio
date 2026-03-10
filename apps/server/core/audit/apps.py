"""Audit app configuration."""

import sys

from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Configuration for the audit logging app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.audit"
    verbose_name = "Audit Logging"

    def ready(self) -> None:
        """Import signals when app is ready."""
        # Skip signal registration during migrations to avoid issues
        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return

        # Import signals to register handlers
        from core.audit import signals  # noqa: F401
