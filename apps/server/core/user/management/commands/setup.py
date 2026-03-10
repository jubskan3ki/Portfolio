"""Django management command for initial setup."""

import os
from collections.abc import Callable

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError


class Command(BaseCommand):
    """Setup command for initializing the application."""

    help = "Initialize application: migrate, create admin, collect static"

    def _get_style(self, name: str) -> Callable[[str], str]:
        """Get style function by name with fallback."""
        return getattr(self.style, name, lambda x: x)

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument("--skip-static", action="store_true", help="Skip static files")
        parser.add_argument("--skip-admin", action="store_true", help="Skip admin creation")

    def handle(self, *_args, **options):
        """Execute the setup command."""
        self.stdout.write("Starting setup...")

        self.run_migrations()

        if not options["skip_admin"]:
            self.create_admin()

        if not options["skip_static"]:
            self.collect_static()

        self.stdout.write(self._get_style("SUCCESS")("Setup completed"))

    def run_migrations(self):
        """Run database migrations."""
        self.stdout.write("Running migrations...")
        try:
            call_command("migrate", verbosity=0)
            self.stdout.write(self._get_style("SUCCESS")("Migrations applied"))
        except (DatabaseError, CommandError) as err:
            self.stdout.write(self._get_style("ERROR")(f"Migration error: {err}"))

    def create_admin(self):
        """Create admin user from environment variables."""
        self.stdout.write("Setting up admin...")

        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not email or not password:
            self.stdout.write(self._get_style("WARNING")("ADMIN_EMAIL/PASSWORD not set"))
            return

        user_model = get_user_model()

        try:
            user, created = user_model.objects.get_or_create(
                email=email,
                defaults={"is_staff": True, "is_superuser": True},
            )

            if not created:
                user.is_staff = True
                user.is_superuser = True

            user.set_password(password)
            user.save()

            action = "created" if created else "updated"
            self.stdout.write(self._get_style("SUCCESS")(f"Admin {action}: {email}"))

        except DatabaseError as err:
            self.stdout.write(self._get_style("ERROR")(f"Admin error: {err}"))

    def collect_static(self):
        """Collect static files."""
        self.stdout.write("Collecting static files...")
        try:
            call_command("collectstatic", verbosity=0, interactive=False, clear=True)
            self.stdout.write(self._get_style("SUCCESS")("Static files collected"))
        except (OSError, CommandError) as err:
            self.stdout.write(self._get_style("ERROR")(f"Static error: {err}"))
