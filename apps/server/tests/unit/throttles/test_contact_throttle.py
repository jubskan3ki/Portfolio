"""Tests unitaires pour le throttle de contact."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from django.core.cache import cache

from core.contact.throttles import ContactsThrottle


class TestContactsThrottleAbuse:
    """Tests pour la detection d'abus du throttle contact."""

    def setup_method(self) -> None:
        cache.clear()

    def test_abuse_counter_increments(self) -> None:
        """Le compteur d'abus s'incremente a chaque appel."""
        throttle = ContactsThrottle()
        request = MagicMock()
        throttle.get_ident = MagicMock(return_value="127.0.0.1")
        request.data = {"email": "test@example.com"}

        throttle._handle_abuse(request)
        assert cache.get("contact_abuse:127.0.0.1") == 1

        throttle._handle_abuse(request)
        assert cache.get("contact_abuse:127.0.0.1") == 2

    def test_abuse_blocks_ip_after_threshold(self) -> None:
        """L'IP est bloquee apres 10 tentatives."""
        throttle = ContactsThrottle()
        request = MagicMock()
        throttle.get_ident = MagicMock(return_value="127.0.0.1")
        request.data = {"email": "abuse@example.com"}

        # Simuler 9 tentatives (pas encore bloque)
        cache.set("contact_abuse:127.0.0.1", 9, 86400)
        throttle._handle_abuse(request)

        # 10eme tentative declenche le blocage
        assert cache.get("contact_abuse_blocked:127.0.0.1") is True

    def test_blocked_ip_denied(self) -> None:
        """Une IP bloquee est refusee par allow_request."""
        throttle = ContactsThrottle()
        request = MagicMock()
        view = MagicMock()
        throttle.get_ident = MagicMock(return_value="10.0.0.1")

        # Bloquer l'IP
        cache.set(key="contact_abuse_blocked:10.0.0.1", value=True, timeout=86400)

        result = throttle.allow_request(request, view)
        assert result is False

    def test_non_blocked_ip_passes_to_parent(self) -> None:
        """Une IP non bloquee passe au throttle parent."""
        throttle = ContactsThrottle()
        request = MagicMock()
        view = MagicMock()
        throttle.get_ident = MagicMock(return_value="10.0.0.2")

        with patch.object(ContactsThrottle.__bases__[0], "allow_request", return_value=True) as mock_parent:
            result = throttle.allow_request(request, view)
            assert result is True
            mock_parent.assert_called_once()
