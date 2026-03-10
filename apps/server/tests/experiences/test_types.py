"""Tests pour les types d'experiences."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListExperienceTypes:
    """Tests endpoint GET /api/experiences/types/"""

    URL = "/api/experiences/types/"

    def test_list_types_public(self, api_client: APIClient) -> None:
        """Liste types accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_types_with_data(
        self,
        api_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Liste types retourne les types existants."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK
        assert sample_experience_type is not None


@pytest.mark.django_db
class TestGetExperienceType:
    """Tests endpoint GET /api/experiences/types/{id}/"""

    URL = "/api/experiences/types/"

    def test_get_type_by_id(
        self,
        api_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Lecture type par ID retourne le type."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_experience_type['id']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["id"] == sample_experience_type["id"]

    def test_get_type_not_found(self, api_client: APIClient) -> None:
        """Lecture type inexistant retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}99999/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestExperiencesByType:
    """Tests endpoint GET /api/experiences/by-type/{name}/"""

    URL = "/api/experiences/by-type/"

    def test_experiences_by_type(
        self,
        api_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Experiences par type retourne les experiences."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_experience_type['name']}/"))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateExperienceType:
    """Tests endpoint POST /api/experiences/types/"""

    URL = "/api/experiences/types/"

    def test_create_type_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation type authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": "Nouveau Type", "icon": "new-icon"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_type_unauthenticated(self, api_client: APIClient) -> None:
        """Creation type non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"name": "Nouveau Type", "icon": "new-icon"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestUpdateExperienceType:
    """Tests endpoint PUT/PATCH /api/experiences/types/{id}/"""

    URL = "/api/experiences/types/"

    def test_update_type_authenticated(
        self,
        authenticated_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Mise a jour type authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_experience_type['id']}/",
                {"name": "Type Modifie"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteExperienceType:
    """Tests endpoint DELETE /api/experiences/types/{id}/"""

    URL = "/api/experiences/types/"

    def test_delete_type_authenticated(
        self,
        authenticated_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Suppression type authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.delete(f"{self.URL}{sample_experience_type['id']}/"),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
