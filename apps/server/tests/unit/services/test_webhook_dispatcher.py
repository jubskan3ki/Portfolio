"""Tests unitaires pour WebhookDispatcher."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from core.webhooks.services.dispatcher import WebhookDispatcher
from tests.factories import WebhookFactory


@pytest.mark.django_db
class TestWebhookToggle:
    """Tests pour WebhookDispatcher.toggle."""

    def test_toggle_activates_inactive_webhook(self, admin_user: Any) -> None:
        """Active un webhook inactif."""
        webhook = WebhookFactory(created_by=admin_user.user, is_active=False)

        result = WebhookDispatcher.toggle(webhook)

        assert result is True
        webhook.refresh_from_db()
        assert webhook.is_active is True

    def test_toggle_deactivates_active_webhook(self, admin_user: Any) -> None:
        """Desactive un webhook actif."""
        webhook = WebhookFactory(created_by=admin_user.user, is_active=True)

        result = WebhookDispatcher.toggle(webhook)

        assert result is False
        webhook.refresh_from_db()
        assert webhook.is_active is False


@pytest.mark.django_db
class TestWebhookDispatch:
    """Tests pour WebhookDispatcher.dispatch."""

    @patch.object(WebhookDispatcher, "send_delivery", return_value=True)
    def test_dispatches_to_subscribed_webhooks(self, mock_send: Any, admin_user: Any) -> None:
        """Envoie aux webhooks abonnes a l'evenement."""
        WebhookFactory(
            created_by=admin_user.user,
            events=["article.created"],
            is_active=True,
        )

        deliveries = WebhookDispatcher.dispatch("article.created", {"title": "Test"})

        assert len(deliveries) == 1
        mock_send.assert_called_once()

    @patch.object(WebhookDispatcher, "send_delivery", return_value=True)
    def test_skips_inactive_webhooks(self, _mock_send: Any, admin_user: Any) -> None:
        """N'envoie pas aux webhooks inactifs."""
        WebhookFactory(
            created_by=admin_user.user,
            events=["article.created"],
            is_active=False,
        )

        deliveries = WebhookDispatcher.dispatch("article.created", {"title": "Test"})

        assert len(deliveries) == 0

    @patch.object(WebhookDispatcher, "send_delivery", return_value=True)
    def test_skips_unsubscribed_events(self, _mock_send: Any, admin_user: Any) -> None:
        """N'envoie pas pour les evenements non abonnes."""
        WebhookFactory(
            created_by=admin_user.user,
            events=["project.created"],
            is_active=True,
        )

        deliveries = WebhookDispatcher.dispatch("article.created", {"title": "Test"})

        assert len(deliveries) == 0


@pytest.mark.django_db
class TestWebhookDispatchAsync:
    """Tests pour WebhookDispatcher.dispatch_async."""

    @patch("core.webhooks.tasks.dispatch_webhook_event")
    def test_dispatches_via_celery(self, mock_task: Any) -> None:
        """Delegue l'envoi a Celery."""
        WebhookDispatcher.dispatch_async("article.created", {"title": "Test"})

        mock_task.delay.assert_called_once()
