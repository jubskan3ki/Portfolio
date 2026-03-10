"""Tests pour les webhooks."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.factories import WebhookFactory


@pytest.mark.django_db
class TestWebhookList:
    """Tests endpoint GET /api/webhooks/ (admin uniquement)."""

    URL = "/api/webhooks/"

    def test_list_webhooks_admin(self, authenticated_client: APIClient, admin_user: Any) -> None:
        """Admin peut lister les webhooks."""
        WebhookFactory(created_by=admin_user.user)
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_webhooks_anonymous_forbidden(self, api_client: APIClient) -> None:
        """Utilisateur anonyme ne peut pas lister les webhooks."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestWebhookCreate:
    """Tests endpoint POST /api/webhooks/."""

    URL = "/api/webhooks/"

    def test_create_webhook_admin(self, authenticated_client: APIClient) -> None:
        """Admin peut creer un webhook."""
        data = {
            "name": "Test Webhook",
            "url": "https://example.com/hook",
            "events": ["article.created"],
        }
        response = cast(Response, authenticated_client.post(self.URL, data, format="json"))

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_webhook_anonymous_forbidden(self, api_client: APIClient) -> None:
        """Utilisateur anonyme ne peut pas creer de webhook."""
        data = {
            "name": "Test Webhook",
            "url": "https://example.com/hook",
            "events": ["article.created"],
        }
        response = cast(Response, api_client.post(self.URL, data, format="json"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestWebhookToggle:
    """Tests endpoint POST /api/webhooks/{id}/toggle/."""

    def test_toggle_webhook_admin(self, authenticated_client: APIClient, admin_user: Any) -> None:
        """Admin peut activer/desactiver un webhook."""
        webhook = WebhookFactory(created_by=admin_user.user)
        url = f"/api/webhooks/{webhook.id}/toggle/"
        response = cast(Response, authenticated_client.post(url))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestWebhookDeliveries:
    """Tests endpoint GET /api/webhooks/{id}/deliveries/."""

    def test_list_deliveries_admin(self, authenticated_client: APIClient, admin_user: Any) -> None:
        """Admin peut lister les livraisons d'un webhook."""
        webhook = WebhookFactory(created_by=admin_user.user)
        url = f"/api/webhooks/{webhook.id}/deliveries/"
        response = cast(Response, authenticated_client.get(url))

        assert response.status_code == status.HTTP_200_OK
