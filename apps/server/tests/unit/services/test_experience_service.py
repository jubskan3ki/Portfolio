"""Tests unitaires pour ExperienceService."""

from __future__ import annotations

from datetime import date

import pytest

from core.experiences.services.experience import ExperienceService
from tests.factories import ExperienceFactory, ExperienceTypeFactory


@pytest.mark.django_db
class TestExperienceServiceGetByType:
    """Tests pour ExperienceService.get_by_type."""

    def test_returns_experiences_for_type(self) -> None:
        """Retourne les experiences du type donne."""
        exp_type = ExperienceTypeFactory(name="CDI")
        ExperienceFactory(type=exp_type)
        ExperienceFactory(type=exp_type)

        result = ExperienceService.get_by_type("CDI")

        assert result.count() == 2

    def test_type_lookup_is_case_insensitive(self) -> None:
        """La recherche par type est insensible a la casse."""
        exp_type = ExperienceTypeFactory(name="Stage")
        ExperienceFactory(type=exp_type)

        result = ExperienceService.get_by_type("stage")

        assert result.count() == 1

    def test_returns_empty_for_nonexistent_type(self) -> None:
        """Retourne un queryset vide pour un type inexistant."""
        result = ExperienceService.get_by_type("Inexistant")

        assert result.count() == 0


@pytest.mark.django_db
class TestExperienceServiceGetCurrent:
    """Tests pour ExperienceService.get_current."""

    def test_returns_current_experience(self) -> None:
        """Retourne l'experience en cours (sans date de fin)."""
        exp_type = ExperienceTypeFactory()
        ExperienceFactory(type=exp_type, end_date=None, start_date=date(2024, 1, 1))

        result = ExperienceService.get_current()

        assert result is not None
        assert result.end_date is None

    def test_returns_none_when_all_completed(self) -> None:
        """Retourne None si toutes les experiences sont terminees."""
        exp_type = ExperienceTypeFactory()
        ExperienceFactory(
            type=exp_type,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
        )

        result = ExperienceService.get_current()

        assert result is None

    def test_returns_latest_current(self) -> None:
        """Retourne l'experience en cours la plus recente."""
        exp_type = ExperienceTypeFactory()
        ExperienceFactory(type=exp_type, end_date=None, start_date=date(2022, 1, 1))
        latest = ExperienceFactory(type=exp_type, end_date=None, start_date=date(2024, 6, 1))

        result = ExperienceService.get_current()

        assert result is not None
        assert result.id == latest.id
