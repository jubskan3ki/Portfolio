"""Tests unitaires pour les serializers d'experiences."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

import pytest
from django.utils import timezone

from core.experiences.serializers.experience import ExperienceWriteSerializer
from tests.factories import ExperienceTypeFactory


@pytest.mark.django_db
class TestExperienceWriteSerializer:
    """Tests pour ExperienceWriteSerializer."""

    def _valid_data(self, experience_type_id: int, **overrides: Any) -> dict:
        base = {
            "title": "Developpeur",
            "company": "Test Corp",
            "location": "Paris",
            "startDate": "2023-01-01",
            "description": "Description de test",
            "type": experience_type_id,
        }
        base.update(overrides)
        return base

    def test_valid_data(self) -> None:
        """Donnees valides passent la validation."""
        exp_type = ExperienceTypeFactory()
        s = ExperienceWriteSerializer(data=self._valid_data(exp_type.id))
        assert s.is_valid(), s.errors

    def test_end_date_before_start_date_rejected(self) -> None:
        """Date de fin anterieure a la date de debut rejetee."""
        exp_type = ExperienceTypeFactory()
        s = ExperienceWriteSerializer(
            data=self._valid_data(
                exp_type.id,
                startDate="2024-01-01",
                endDate="2023-01-01",
            )
        )
        assert not s.is_valid()
        assert "endDate" in s.errors

    def test_future_start_date_rejected(self) -> None:
        """Date de debut dans le futur rejetee."""
        exp_type = ExperienceTypeFactory()
        future = (timezone.now().date() + timedelta(days=30)).isoformat()
        s = ExperienceWriteSerializer(data=self._valid_data(exp_type.id, startDate=future))
        assert not s.is_valid()
        assert "startDate" in s.errors

    def test_today_start_date_accepted(self) -> None:
        """Date de debut aujourd'hui acceptee."""
        exp_type = ExperienceTypeFactory()
        today = timezone.now().date().isoformat()
        s = ExperienceWriteSerializer(data=self._valid_data(exp_type.id, startDate=today))
        assert s.is_valid(), s.errors

    def test_null_end_date_accepted(self) -> None:
        """Date de fin null acceptee (experience en cours)."""
        exp_type = ExperienceTypeFactory()
        s = ExperienceWriteSerializer(data=self._valid_data(exp_type.id, endDate=None))
        assert s.is_valid(), s.errors
