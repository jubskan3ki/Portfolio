"""Tests unitaires pour PasswordService."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from django.core.exceptions import PermissionDenied

from core.user.services.password import PasswordService
from tests.factories import UserFactory


class TestGenerateResetCode:
    """Tests pour PasswordService.generate_reset_code."""

    def test_generates_code_of_correct_length(self) -> None:
        """Le code genere a la bonne longueur."""
        code = PasswordService.generate_reset_code()

        assert len(code) == 8

    def test_generates_alphanumeric_uppercase_code(self) -> None:
        """Le code ne contient que des majuscules et chiffres."""
        code = PasswordService.generate_reset_code()

        assert code == code.upper()
        assert code.isalnum()

    def test_generates_unique_codes(self) -> None:
        """Deux codes generes sont differents."""
        codes = {PasswordService.generate_reset_code() for _ in range(10)}

        assert len(codes) > 1


@pytest.mark.django_db
class TestChangePassword:
    """Tests pour PasswordService.change_password."""

    def test_changes_password_with_valid_data(self) -> None:
        """Change le mot de passe avec des donnees valides."""
        user = UserFactory()
        user.set_password("OldPassword123!")
        user.save()

        result = PasswordService.change_password(user, "OldPassword123!", "NewPassword456!")

        assert result is True
        user.refresh_from_db()
        assert user.check_password("NewPassword456!")

    def test_rejects_wrong_old_password(self) -> None:
        """Rejette si l'ancien mot de passe est incorrect."""
        user = UserFactory()
        user.set_password("OldPassword123!")
        user.save()

        with pytest.raises(PermissionDenied):
            PasswordService.change_password(user, "WrongPassword!", "NewPassword456!")

    def test_rejects_same_password(self) -> None:
        """Rejette si le nouveau mot de passe est identique a l'ancien."""
        user = UserFactory()
        user.set_password("SamePassword123!")
        user.save()

        with pytest.raises(PermissionDenied):
            PasswordService.change_password(user, "SamePassword123!", "SamePassword123!")


@pytest.mark.django_db
class TestRequestPasswordReset:
    """Tests pour PasswordService.request_password_reset."""

    @patch("core.user.services.password.PasswordService._ensure_min_response_time")
    @patch("core.user.services.password.PasswordService._send_reset_email")
    def test_returns_true_for_existing_user(self, _mock_send, _mock_timing) -> None:
        """Retourne True pour un utilisateur existant."""
        UserFactory(email="test@example.com")

        result = PasswordService.request_password_reset("test@example.com")

        assert result is True

    @patch("core.user.services.password.PasswordService._ensure_min_response_time")
    def test_returns_true_for_nonexistent_email(self, _mock_timing) -> None:
        """Retourne True meme pour un email inexistant (securite)."""
        result = PasswordService.request_password_reset("nonexistent@example.com")

        assert result is True
