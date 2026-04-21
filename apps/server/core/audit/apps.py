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
        # Evite l'enregistrement pendant migrate/makemigrations (FK sur AUTH_USER_MODEL).
        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return

        from core.audit import signals

        _ = signals
