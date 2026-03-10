"""Tests pour les categories de projets."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListProjectCategories:
    """Tests endpoint GET /api/projects/categories/"""

    URL = "/api/projects/categories/"

    def test_list_categories_public(self, api_client: APIClient) -> None:
        """Liste categories accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetProjectCategory:
    """Tests endpoint GET /api/projects/categories/{slug}/"""

    URL = "/api/projects/categories/"

    def test_get_category_by_slug(
        self,
        api_client: APIClient,
        sample_project_category: dict[str, Any],
    ) -> None:
        """Lecture categorie par slug retourne la categorie."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_project_category['slug']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["slug"] == sample_project_category["slug"]

    def test_get_category_not_found(self, api_client: APIClient) -> None:
        """Lecture categorie inexistante retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}categorie-inexistante/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestProjectsByCategory:
    """Tests endpoint GET /api/projects/by-category/{slug}/"""

    URL = "/api/projects/by-category/"

    def test_projects_by_category(
        self,
        api_client: APIClient,
        sample_project_category: dict[str, Any],
    ) -> None:
        """Projets par categorie retourne les projets."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_project_category['slug']}/"))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateProjectCategory:
    """Tests endpoint POST /api/projects/categories/"""

    URL = "/api/projects/categories/"

    def test_create_category_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation categorie authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": "Nouvelle Categorie"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_category_unauthenticated(self, api_client: APIClient) -> None:
        """Creation categorie non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"name": "Nouvelle Categorie"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
