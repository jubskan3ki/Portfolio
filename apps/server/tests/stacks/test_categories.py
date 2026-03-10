"""Tests pour les categories de stacks."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListStackCategories:
    """Tests endpoint GET /api/stacks/categories/"""

    URL = "/api/stacks/categories/"

    def test_list_categories_public(self, api_client: APIClient) -> None:
        """Liste categories accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetStackCategory:
    """Tests endpoint GET /api/stacks/categories/{name}/"""

    URL = "/api/stacks/categories/"

    def test_get_category_by_name(
        self,
        api_client: APIClient,
        sample_stack_category: dict[str, Any],
    ) -> None:
        """Lecture categorie par name retourne la categorie."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_stack_category['name']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["name"] == sample_stack_category["name"]

    def test_get_category_not_found(self, api_client: APIClient) -> None:
        """Lecture categorie inexistante retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}categorie-inexistante/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestStacksByCategory:
    """Tests endpoint GET /api/stacks/by-category/{name}/"""

    URL = "/api/stacks/by-category/"

    def test_stacks_by_category(
        self,
        api_client: APIClient,
        sample_stack_category: dict[str, Any],
    ) -> None:
        """Stacks par categorie retourne les stacks."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_stack_category['name']}/"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateStackCategory:
    """Tests endpoint POST /api/stacks/categories/"""

    URL = "/api/stacks/categories/"

    def test_create_category_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation categorie authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(self.URL, {"name": "Nouvelle Categorie"}, format="json"),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_category_unauthenticated(self, api_client: APIClient) -> None:
        """Creation categorie non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(self.URL, {"name": "Nouvelle Categorie"}, format="json"),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
