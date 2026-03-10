"""Tests pour les ressources de stacks."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListStackResources:
    """Tests endpoint GET /api/stacks/resources/"""

    URL = "/api/stacks/resources/"

    def test_list_resources_public(self, api_client: APIClient) -> None:
        """Liste ressources accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateStackResource:
    """Tests endpoint POST /api/stacks/resources/"""

    URL = "/api/stacks/resources/"

    def test_create_resource_authenticated(
        self,
        authenticated_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Creation ressource authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "title": "Nouvelle Ressource",
                    "description": "Description de la ressource",
                    "url": "https://example.com",
                    "stack": sample_stack["id"],
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_resource_unauthenticated(
        self,
        api_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Creation ressource non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "title": "Nouvelle Ressource",
                    "url": "https://example.com",
                    "stack": sample_stack["id"],
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_resource_invalid_url(
        self,
        authenticated_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Creation ressource avec URL invalide retourne 400."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "title": "Ressource",
                    "description": "Description",
                    "url": "not-a-valid-url",
                    "stack": sample_stack["id"],
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
