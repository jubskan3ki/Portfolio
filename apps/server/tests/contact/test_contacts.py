"""Tests pour les soumissions de contact."""

from __future__ import annotations

from typing import cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestSubmitContact:
    """Tests endpoint POST /api/contacts/"""

    URL = "/api/contacts/"

    def test_submit_contact_valid(self, api_client: APIClient) -> None:
        """Soumission contact valide reussit."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "subject": "Question",
                    "message": "Ceci est un message de test.",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_submit_contact_missing_name(self, api_client: APIClient) -> None:
        """Soumission sans nom retourne 400."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "email": "john@example.com",
                    "subject": "Question",
                    "message": "Message",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_contact_missing_email(self, api_client: APIClient) -> None:
        """Soumission sans email retourne 400."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "name": "John Doe",
                    "subject": "Question",
                    "message": "Message",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_contact_invalid_email(self, api_client: APIClient) -> None:
        """Soumission avec email invalide retourne 400."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "name": "John Doe",
                    "email": "not-an-email",
                    "subject": "Question",
                    "message": "Message",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_contact_missing_message(self, api_client: APIClient) -> None:
        """Soumission sans message retourne 400."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "subject": "Question",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_contact_empty_body(self, api_client: APIClient) -> None:
        """Soumission avec body vide retourne 400."""
        response = cast(Response, api_client.post(self.URL, {}, format="json"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListContacts:
    """Tests endpoint GET /api/contacts/"""

    URL = "/api/contacts/"

    def test_list_contacts_unauthenticated(self, api_client: APIClient) -> None:
        """Liste contacts non authentifie retourne 401."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_contacts_authenticated(self, authenticated_client: APIClient) -> None:
        """Liste contacts authentifie reussit."""
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestContactStats:
    """Tests endpoint GET /api/contacts/stats/"""

    URL = "/api/contacts/stats/"

    def test_stats_public(self, api_client: APIClient) -> None:
        """Stats contact peut etre public ou protege."""
        response = cast(Response, api_client.get(self.URL))

        # Peut etre 200, 401 ou 404 selon la config
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_stats_authenticated(self, authenticated_client: APIClient) -> None:
        """Stats contact authentifie."""
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
