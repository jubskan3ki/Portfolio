"""Tests pour le modele User | contrainte unicite superuser."""

from __future__ import annotations

from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
def test_single_superuser_allowed(db: Any) -> None:
    """Un superuser peut etre cree normalement."""
    del db
    user = User.objects.create_superuser(
        email="super1@example.com",
        password="TestPass123!",
    )
    assert user.is_superuser is True
    assert User.objects.filter(is_superuser=True).count() == 1


@pytest.mark.django_db
def test_second_superuser_blocked_by_save(db: Any) -> None:
    """Le save() Python empeche un second superuser avec un message lisible."""
    del db
    # Create the first superuser directly (not via fixture to avoid conflicts)
    User.objects.create_superuser(
        email="super_first@example.com",
        password="TestPass123!",
    )
    # Bypass manager check to test model save() validation directly
    user2 = User(email="super2@example.com", is_superuser=True, is_staff=True, is_active=True)
    user2.set_password("TestPass123!")
    with pytest.raises(ValidationError, match="Un seul superuser"):
        user2.save()


@pytest.mark.django_db(transaction=True)
def test_second_superuser_blocked_by_db_constraint(db: Any) -> None:
    """La contrainte DB empeche un second superuser meme sans save()."""
    del db
    # Create the first superuser directly
    User.objects.create_superuser(
        email="super_constraint@example.com",
        password="TestPass123!",
    )
    # Contourner save() en inserant directement via bulk_create
    try:
        User.objects.bulk_create(
            [
                User(
                    email="super_bypass@example.com",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                )
            ]
        )
        pytest.fail("La contrainte DB aurait du empecher la creation")
    except IntegrityError:
        pass  # Attendu : la contrainte unique_superuser bloque l'insertion
