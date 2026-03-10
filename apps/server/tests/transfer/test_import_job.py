"""Tests pour ImportJob — plafonnement des erreurs."""

from __future__ import annotations

from typing import Any

import pytest
from django.contrib.auth import get_user_model

from core.transfer.models import ImportJob

User = get_user_model()


@pytest.fixture
def import_job(admin_user: Any) -> ImportJob:
    """Cree un ImportJob de test."""
    return ImportJob.objects.create(
        user=admin_user.user,
        module="articles",
        original_filename="test.json",
        file_format="json",
        total_records=2000,
    )


@pytest.mark.django_db
def test_add_error_accumulates(import_job: ImportJob) -> None:
    """Les erreurs s'accumulent normalement sous le plafond."""
    for i in range(10):
        import_job.add_error(row=i, field="title", message=f"Erreur {i}")

    assert import_job.error_count == 10
    assert len(import_job.errors) == 10


@pytest.mark.django_db
def test_add_error_capped_at_max(import_job: ImportJob) -> None:
    """Les erreurs sont plafonnees a MAX_STORED_ERRORS + 1 (message de troncature)."""
    for i in range(1000):
        import_job.add_error(row=i, field="title", message=f"Erreur {i}")

    # error_count reflete le total reel
    assert import_job.error_count == 1000
    # La liste JSON est plafonnee a MAX_STORED_ERRORS + 1 (troncature incluse)
    assert len(import_job.errors) == ImportJob.MAX_STORED_ERRORS + 1


@pytest.mark.django_db
def test_add_error_truncation_message(import_job: ImportJob) -> None:
    """Un message de troncature est ajoute quand le plafond est atteint."""
    for i in range(ImportJob.MAX_STORED_ERRORS + 50):
        import_job.add_error(row=i, field="title", message=f"Erreur {i}")

    last_error = import_job.errors[-1]
    assert last_error["field"] == "_truncated"
    assert str(ImportJob.MAX_STORED_ERRORS) in last_error["message"]


@pytest.mark.django_db
def test_add_error_count_always_accurate(import_job: ImportJob) -> None:
    """error_count reste exact meme apres troncature."""
    total = 750
    for i in range(total):
        import_job.add_error(row=i, field="name", message=f"Invalide {i}")

    assert import_job.error_count == total
    assert len(import_job.errors) <= ImportJob.MAX_STORED_ERRORS + 1
