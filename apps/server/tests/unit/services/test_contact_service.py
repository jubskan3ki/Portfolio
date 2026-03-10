"""Tests unitaires pour ContactService."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from core.contact.models import Contact
from core.contact.services.contact import ContactService


@pytest.mark.django_db
class TestContactServiceSubmitForm:
    """Tests pour ContactService.submit_form()."""

    def _valid_data(self, **overrides) -> dict:
        base = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Question",
            "message": "Un message de test.",
        }
        base.update(overrides)
        return base

    @patch("core.contact.services.contact.send_admin_notification")
    @patch("core.contact.services.contact.send_user_confirmation")
    def test_creates_contact(self, _mock_confirm, _mock_notify) -> None:
        """submit_form cree un Contact en base."""
        ref = ContactService.submit_form(data=self._valid_data(), ip_address="127.0.0.1")

        assert isinstance(ref, str)
        assert len(ref) == 8
        assert Contact.objects.filter(reference_id=ref).exists()

    @patch("core.contact.services.contact.send_admin_notification")
    @patch("core.contact.services.contact.send_user_confirmation")
    def test_stores_ip_address(self, _mock_confirm, _mock_notify) -> None:
        """submit_form enregistre l'adresse IP."""
        ref = ContactService.submit_form(data=self._valid_data(), ip_address="192.168.1.1")

        contact = Contact.objects.get(reference_id=ref)
        assert contact.ip_address == "192.168.1.1"

    @patch("core.contact.services.contact.send_admin_notification")
    @patch("core.contact.services.contact.send_user_confirmation")
    def test_returns_unique_reference_ids(self, _mock_confirm, _mock_notify) -> None:
        """Chaque soumission a un reference_id unique."""
        ref1 = ContactService.submit_form(data=self._valid_data())
        ref2 = ContactService.submit_form(data=self._valid_data(email="other@example.com"))

        assert ref1 != ref2

    @patch("core.contact.services.contact.send_admin_notification")
    @patch("core.contact.services.contact.send_user_confirmation")
    def test_filters_extra_fields(self, _mock_confirm, _mock_notify) -> None:
        """Les champs non-modele (recaptchaToken) sont ignores."""
        data = self._valid_data(recaptchaToken="fake-token")
        ref = ContactService.submit_form(data=data)

        contact = Contact.objects.get(reference_id=ref)
        assert contact.name == "John Doe"

    @patch("core.contact.services.contact.send_admin_notification")
    @patch("core.contact.services.contact.send_user_confirmation")
    def test_optional_phone_and_company(self, _mock_confirm, _mock_notify) -> None:
        """Les champs optionnels phone et company sont enregistres."""
        data = self._valid_data(phone="+33612345678", company="Test Corp")
        ref = ContactService.submit_form(data=data)

        contact = Contact.objects.get(reference_id=ref)
        assert contact.phone == "+33612345678"
        assert contact.company == "Test Corp"
