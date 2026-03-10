"""Create or update admin user."""

import os
import sys
from pathlib import Path

from django.db import DatabaseError, IntegrityError

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model

user_model = get_user_model()


def main():
    """Create or update admin user from environment variables."""
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")

    if not email or not password:
        print("ERROR: ADMIN_EMAIL or ADMIN_PASSWORD not set")
        return 1

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
        print(f"Admin user {action}: {email}")
        return 0

    except (DatabaseError, IntegrityError, ValueError, TypeError) as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
