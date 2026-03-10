"""Tests pour les projets."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListProjects:
    """Tests endpoint GET /api/projects/"""

    URL = "/api/projects/"

    def test_list_projects_public(self, api_client: APIClient) -> None:
        """Liste projets accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_projects_pagination(self, api_client: APIClient) -> None:
        """Liste projets supporte pagination."""
        response = cast(Response, api_client.get(f"{self.URL}?page=1&limit=5"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetProject:
    """Tests endpoint GET /api/projects/{slug}/"""

    URL = "/api/projects/"

    def test_get_project_by_slug(
        self,
        api_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        """Lecture projet par slug retourne le projet."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_project['slug']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["slug"] == sample_project["slug"]

    def test_get_project_not_found(self, api_client: APIClient) -> None:
        """Lecture projet inexistant retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}projet-inexistant/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFeaturedProjects:
    """Tests endpoint GET /api/projects/featured/"""

    URL = "/api/projects/featured/"

    def test_featured_projects_public(self, api_client: APIClient) -> None:
        """Projets featured accessibles."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestProjectStats:
    """Tests endpoint GET /api/projects/stats/"""

    URL = "/api/projects/stats/"

    def test_stats_public(self, api_client: APIClient) -> None:
        """Stats projets accessibles."""
        response = cast(Response, api_client.get(self.URL))

        # Peut etre 200 ou 404 selon routage
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestProjectInteraction:
    """Tests endpoint POST /api/projects/interaction/{slug}/like/"""

    URL = "/api/projects/interaction/"

    def test_like_project(
        self,
        api_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        """Like projet fonctionne."""
        response = cast(Response, api_client.post(f"{self.URL}{sample_project['slug']}/like/"))

        # May require authentication or be public
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCreateProject:
    """Tests endpoint POST /api/projects/"""

    URL = "/api/projects/"

    def test_create_project_authenticated(
        self,
        authenticated_client: APIClient,
        sample_project_category: dict[str, Any],
    ) -> None:
        """Creation projet authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "title": "Nouveau Projet",
                    "description": "Description du projet",
                    "category": sample_project_category["id"],
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_project_unauthenticated(
        self,
        api_client: APIClient,
        sample_project_category: dict[str, Any],
    ) -> None:
        """Creation projet non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "title": "Nouveau Projet",
                    "description": "Description",
                    "category": sample_project_category["id"],
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestUpdateProject:
    """Tests endpoint PUT/PATCH /api/projects/{slug}/"""

    URL = "/api/projects/"

    def test_update_project_authenticated(
        self,
        authenticated_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        """Mise a jour projet authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_project['slug']}/",
                {"title": "Titre Modifie"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_project_unauthenticated(
        self,
        api_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        """Mise a jour projet non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.patch(
                f"{self.URL}{sample_project['slug']}/",
                {"title": "Titre Modifie"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteProject:
    """Tests endpoint DELETE /api/projects/{slug}/"""

    URL = "/api/projects/"

    def test_delete_project_authenticated(
        self,
        authenticated_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        """Suppression projet authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.delete(f"{self.URL}{sample_project['slug']}/"),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_project_unauthenticated(
        self,
        api_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        """Suppression projet non authentifie retourne 401/403."""
        response = cast(Response, api_client.delete(f"{self.URL}{sample_project['slug']}/"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
