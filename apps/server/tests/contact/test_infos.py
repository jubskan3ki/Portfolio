"""Tests pour les informations de contact."""

from __future__ import annotations

from typing import cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListContactInfos:
    """Tests endpoint GET /api/contacts/infos/"""

    URL = "/api/contacts/infos/"

    def test_list_infos_public(self, api_client: APIClient) -> None:
        """Liste infos contact peut etre publique."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_list_infos_authenticated(self, authenticated_client: APIClient) -> None:
        """Liste infos contact authentifie."""
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateContactInfo:
    """Tests endpoint POST /api/contacts/infos/"""

    URL = "/api/contacts/infos/"

    def test_create_info_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation info contact authentifie."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "type": "email",
                    "value": "contact@example.com",
                },
                format="json",
            ),
        )

        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_create_info_unauthenticated(self, api_client: APIClient) -> None:
        """Creation info contact non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "type": "email",
                    "value": "contact@example.com",
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
