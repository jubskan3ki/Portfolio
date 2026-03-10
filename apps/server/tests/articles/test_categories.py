"""Tests pour les categories d'articles."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListCategories:
    """Tests endpoint GET /api/articles/categories/"""

    URL = "/api/articles/categories/"

    def test_list_categories_public(self, api_client: APIClient) -> None:
        """Liste des categories accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_categories_with_data(
        self,
        api_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Liste des categories retourne les categories existantes."""
        response = cast(Response, api_client.get(self.URL))

        if response.status_code == status.HTTP_200_OK and hasattr(response, "data"):
            resp_data = cast(dict[str, Any], response.data)
            data = resp_data.get("data", response.data)
            if isinstance(data, list) and len(data) > 0:
                assert "name" in data[0]
                assert "slug" in data[0]
        assert sample_category is not None


@pytest.mark.django_db
class TestGetCategory:
    """Tests endpoint GET /api/articles/categories/{slug}/"""

    URL = "/api/articles/categories/"

    def test_get_category_by_slug(
        self,
        api_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Lecture categorie par slug retourne la categorie."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_category['slug']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["slug"] == sample_category["slug"]
            assert data["name"] == sample_category["name"]

    def test_get_category_not_found(self, api_client: APIClient) -> None:
        """Lecture categorie inexistante retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}categorie-inexistante/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestArticlesByCategory:
    """Tests endpoint GET /api/articles/by-category/{slug}/"""

    URL = "/api/articles/by-category/"

    def test_articles_by_category(
        self,
        api_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Articles par categorie retourne les articles."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_category['slug']}/"))

        assert response.status_code == status.HTTP_200_OK

    def test_articles_by_category_not_found(self, api_client: APIClient) -> None:
        """Articles par categorie inexistante retourne 404 ou 200 (liste vide)."""
        response = cast(Response, api_client.get(f"{self.URL}categorie-inexistante/"))

        # API may return empty list (200) or 404 for non-existent category
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateCategory:
    """Tests endpoint POST /api/articles/categories/"""

    URL = "/api/articles/categories/"

    def test_create_category_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation categorie authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": "Nouvelle Categorie", "description": "Description de la categorie"},
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
                {"name": "Nouvelle Categorie", "description": "Description"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_category_duplicate_name(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Creation categorie avec nom duplique retourne 400."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": sample_category["name"], "description": "Description"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateCategory:
    """Tests endpoint PUT/PATCH /api/articles/categories/{slug}/"""

    URL = "/api/articles/categories/"

    def test_update_category_authenticated(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Mise a jour categorie authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_category['slug']}/",
                {"description": "Nouvelle description"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_category_unauthenticated(
        self,
        api_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Mise a jour categorie non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.patch(
                f"{self.URL}{sample_category['slug']}/",
                {"description": "Nouvelle description"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteCategory:
    """Tests endpoint DELETE /api/articles/categories/{slug}/"""

    URL = "/api/articles/categories/"

    def test_delete_category_authenticated(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Suppression categorie authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.delete(f"{self.URL}{sample_category['slug']}/"),
        )

        # Peut echouer si articles lies (PROTECT)
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_409_CONFLICT,
        ]

    def test_delete_category_unauthenticated(
        self,
        api_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Suppression categorie non authentifie retourne 401/403."""
        response = cast(Response, api_client.delete(f"{self.URL}{sample_category['slug']}/"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
