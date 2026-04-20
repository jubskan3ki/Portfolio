"""Django management command for health checks."""

import json
from collections.abc import Callable

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import DatabaseError, connection
from kombu import Connection
from kombu.exceptions import KombuError


class Command(BaseCommand):
    """Health check command for monitoring."""

    help = "Check application health: database, cache, broker."

    def _get_style(self, name: str) -> Callable[[str], str]:
        """Get style function by name with fallback."""
        return getattr(self.style, name, lambda x: x)

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument("--json", action="store_true", help="Output as JSON")

    def handle(self, *_args, **options):
        """Execute the health check command."""
        results = {
            "database": self.check_database(),
            "cache": self.check_cache(),
            "broker": self.check_broker(),
        }

        if options["json"]:
            self.stdout.write(json.dumps(results))
        else:
            for service, status in results.items():
                style_name = "SUCCESS" if status["ok"] else "ERROR"
                style_func = self._get_style(style_name)
                self.stdout.write(style_func(f"{service}: {status['message']}"))

        all_ok = all(r["ok"] for r in results.values())
        return None if all_ok else "Health check failed"

    def check_database(self):
        """Check database connection."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except DatabaseError as err:
            return {"ok": False, "message": str(err)}
        else:
            return {"ok": True, "message": "Connected"}

    def check_cache(self):
        """Check cache connection."""
        try:
            cache.set("healthcheck", "ok", 10)
            value = cache.get("healthcheck")
        except (ConnectionError, OSError, ValueError) as err:
            return {"ok": False, "message": str(err)}
        else:
            if value == "ok":
                return {"ok": True, "message": "Connected"}
            return {"ok": False, "message": "Cache read failed"}

    def check_broker(self):
        """Check Celery broker connectivity."""
        broker_url = getattr(settings, "CELERY_BROKER_URL", "")
        if not broker_url:
            return {"ok": True, "message": "No broker configured (skipped)"}
        try:
            with Connection(broker_url, connect_timeout=2) as conn:
                conn.ensure_connection(max_retries=1, interval_start=0, interval_step=0)
        except (KombuError, OSError) as err:
            return {"ok": False, "message": str(err)}
        else:
            return {"ok": True, "message": "Connected"}
