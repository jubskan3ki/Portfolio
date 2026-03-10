"""Tests unitaires pour les serializers de contact."""

from __future__ import annotations

import pytest

from core.contact.serializers.contact import ContactSerializer


@pytest.mark.django_db
class TestContactSerializer:
    """Tests pour ContactSerializer."""

    def _valid_data(self, **overrides) -> dict:
        base = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Question",
            "message": "Ceci est un message de test suffisamment long.",
        }
        base.update(overrides)
        return base

    def test_valid_data(self) -> None:
        """Donnees valides passent la validation."""
        s = ContactSerializer(data=self._valid_data())
        assert s.is_valid(), s.errors

    def test_email_normalized(self) -> None:
        """Email est normalise en minuscules."""
        s = ContactSerializer(data=self._valid_data(email="  John@EXAMPLE.com  "))
        assert s.is_valid(), s.errors
        assert s.validated_data["email"] == "john@example.com"

    def test_name_too_short(self) -> None:
        """Nom de moins de 2 caracteres rejete."""
        s = ContactSerializer(data=self._valid_data(name="J"))
        assert not s.is_valid()
        assert "name" in s.errors

    def test_name_empty_after_strip(self) -> None:
        """Nom vide apres nettoyage rejete."""
        s = ContactSerializer(data=self._valid_data(name="   "))
        assert not s.is_valid()
        assert "name" in s.errors

    def test_message_too_short(self) -> None:
        """Message de moins de 10 caracteres rejete."""
        s = ContactSerializer(data=self._valid_data(message="Court"))
        assert not s.is_valid()
        assert "message" in s.errors

    def test_message_max_length(self) -> None:
        """Message depassant 5000 caracteres rejete."""
        s = ContactSerializer(data=self._valid_data(message="x" * 5001))
        assert not s.is_valid()
        assert "message" in s.errors

    def test_message_at_max_length(self) -> None:
        """Message de exactement 5000 caracteres accepte."""
        s = ContactSerializer(data=self._valid_data(message="x" * 5000))
        assert s.is_valid(), s.errors

    def test_invalid_email(self) -> None:
        """Email invalide rejete."""
        s = ContactSerializer(data=self._valid_data(email="not-an-email"))
        assert not s.is_valid()
        assert "email" in s.errors

    def test_missing_required_fields(self) -> None:
        """Champs requis manquants rejetes."""
        s = ContactSerializer(data={})
        assert not s.is_valid()
        for field in ("name", "email", "subject", "message"):
            assert field in s.errors
