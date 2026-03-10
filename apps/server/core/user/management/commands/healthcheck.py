"""Django management command for health checks."""

import json
from collections.abc import Callable

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import DatabaseError, connection


class Command(BaseCommand):
    """Health check command for monitoring."""

    help = "Check application health: database, cache, etc."

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
