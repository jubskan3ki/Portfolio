"""Tests pour les statuts de projets."""

from __future__ import annotations

from typing import cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListProjectStatuses:
    """Tests endpoint GET /api/projects/statuses/"""

    URL = "/api/projects/statuses/"

    def test_list_statuses_public(self, api_client: APIClient) -> None:
        """Liste statuts accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateProjectStatus:
    """Tests endpoint POST /api/projects/statuses/"""

    URL = "/api/projects/statuses/"

    def test_create_status_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation statut authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": "Nouveau Statut", "color": "#FF0000"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_status_unauthenticated(self, api_client: APIClient) -> None:
        """Creation statut non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"name": "Nouveau Statut", "color": "#FF0000"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
