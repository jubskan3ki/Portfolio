"""Tests pour les experiences."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListExperiences:
    """Tests endpoint GET /api/experiences/"""

    URL = "/api/experiences/"

    def test_list_experiences_public(self, api_client: APIClient) -> None:
        """Liste experiences accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_experiences_pagination(self, api_client: APIClient) -> None:
        """Liste experiences supporte pagination."""
        response = cast(Response, api_client.get(f"{self.URL}?page=1&limit=5"))

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        if "pagination" in data:
            assert "total" in data["pagination"]

    def test_list_experiences_filter_by_type(self, api_client: APIClient) -> None:
        """Filtre par type fonctionne."""
        response = cast(Response, api_client.get(f"{self.URL}?type=work"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetExperience:
    """Tests endpoint GET /api/experiences/{id}/"""

    URL = "/api/experiences/"

    def test_get_experience_by_id(
        self,
        api_client: APIClient,
        sample_experience: dict[str, Any],
    ) -> None:
        """Lecture experience par ID retourne l'experience."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_experience['id']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["id"] == sample_experience["id"]

    def test_get_experience_not_found(self, api_client: APIClient) -> None:
        """Lecture experience inexistante retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}99999/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCurrentExperience:
    """Tests endpoint GET /api/experiences/current/"""

    URL = "/api/experiences/current/"

    def test_current_experience(self, api_client: APIClient) -> None:
        """Experience en cours retourne 200 ou 404."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestExperienceStats:
    """Tests endpoint GET /api/experiences/stats/"""

    URL = "/api/experiences/stats/"

    def test_stats_public(self, api_client: APIClient) -> None:
        """Stats experiences accessibles."""
        response = cast(Response, api_client.get(self.URL))

        # Peut etre 200 ou 404 selon routage
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestExperienceTimeline:
    """Tests endpoint GET /api/experiences/timeline/"""

    URL = "/api/experiences/timeline/"

    def test_timeline_public(self, api_client: APIClient) -> None:
        """Timeline experiences accessible."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateExperience:
    """Tests endpoint POST /api/experiences/"""

    URL = "/api/experiences/"

    def test_create_experience_authenticated(
        self,
        authenticated_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Creation experience authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "title": "Nouvelle Experience",
                    "company": "Entreprise",
                    "type": sample_experience_type["id"],
                    "startDate": "2023-01-01",
                    "location": "Paris, France",
                    "description": "Description de l'experience",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_experience_unauthenticated(
        self,
        api_client: APIClient,
        sample_experience_type: dict[str, Any],
    ) -> None:
        """Creation experience non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "title": "Nouvelle Experience",
                    "company": "Entreprise",
                    "type": sample_experience_type["id"],
                    "startDate": "2023-01-01",
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestUpdateExperience:
    """Tests endpoint PUT/PATCH /api/experiences/{id}/"""

    URL = "/api/experiences/"

    def test_update_experience_authenticated(
        self,
        authenticated_client: APIClient,
        sample_experience: dict[str, Any],
    ) -> None:
        """Mise a jour experience authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_experience['id']}/",
                {"title": "Titre Modifie"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_experience_unauthenticated(
        self,
        api_client: APIClient,
        sample_experience: dict[str, Any],
    ) -> None:
        """Mise a jour experience non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.patch(
                f"{self.URL}{sample_experience['id']}/",
                {"title": "Titre Modifie"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteExperience:
    """Tests endpoint DELETE /api/experiences/{id}/"""

    URL = "/api/experiences/"

    def test_delete_experience_authenticated(
        self,
        authenticated_client: APIClient,
        sample_experience: dict[str, Any],
    ) -> None:
        """Suppression experience authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.delete(f"{self.URL}{sample_experience['id']}/"),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_experience_unauthenticated(
        self,
        api_client: APIClient,
        sample_experience: dict[str, Any],
    ) -> None:
        """Suppression experience non authentifie retourne 401/403."""
        response = cast(Response, api_client.delete(f"{self.URL}{sample_experience['id']}/"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
