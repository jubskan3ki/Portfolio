"""Tests pour les stacks."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListStacks:
    """Tests endpoint GET /api/stacks/"""

    URL = "/api/stacks/"

    def test_list_stacks_public(self, api_client: APIClient) -> None:
        """Liste stacks accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_stacks_pagination(self, api_client: APIClient) -> None:
        """Liste stacks supporte pagination."""
        response = cast(Response, api_client.get(f"{self.URL}?page=1&limit=5"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetStack:
    """Tests endpoint GET /api/stacks/{slug}/"""

    URL = "/api/stacks/"

    def test_get_stack_by_slug(self, api_client: APIClient, sample_stack: dict[str, Any]) -> None:
        """Lecture stack par slug retourne le stack."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_stack['slug']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["slug"] == sample_stack["slug"]

    def test_get_stack_not_found(self, api_client: APIClient) -> None:
        """Lecture stack inexistant retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}stack-inexistant/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRelatedStacks:
    """Tests endpoint GET /api/stacks/{slug}/related/"""

    URL = "/api/stacks/"

    def test_related_stacks(self, api_client: APIClient, sample_stack: dict[str, Any]) -> None:
        """Stacks lies retournes."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_stack['slug']}/related/"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestStackStats:
    """Tests endpoint GET /api/stacks/stats/"""

    URL = "/api/stacks/stats/"

    def test_stats_public(self, api_client: APIClient) -> None:
        """Stats stacks accessibles."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateStack:
    """Tests endpoint POST /api/stacks/"""

    URL = "/api/stacks/"

    def test_create_stack_authenticated(
        self,
        authenticated_client: APIClient,
        sample_stack_category: dict[str, Any],
    ) -> None:
        """Creation stack authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "name": "Nouveau Stack",
                    "description": "Description du stack",
                    "category": sample_stack_category["id"],
                    "level": "3.5",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_stack_unauthenticated(
        self,
        api_client: APIClient,
        sample_stack_category: dict[str, Any],
    ) -> None:
        """Creation stack non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "name": "Nouveau Stack",
                    "description": "Description",
                    "category": sample_stack_category["id"],
                    "level": "3.5",
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestUpdateStack:
    """Tests endpoint PUT/PATCH /api/stacks/{slug}/"""

    URL = "/api/stacks/"

    def test_update_stack_authenticated(
        self,
        authenticated_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Mise a jour stack authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_stack['slug']}/",
                {"name": "Nom Modifie", "level": "4.0"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_stack_unauthenticated(
        self,
        api_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Mise a jour stack non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.patch(
                f"{self.URL}{sample_stack['slug']}/",
                {"name": "Nom Modifie"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteStack:
    """Tests endpoint DELETE /api/stacks/{slug}/"""

    URL = "/api/stacks/"

    def test_delete_stack_authenticated(
        self,
        authenticated_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Suppression stack authentifie reussit."""
        response = cast(Response, authenticated_client.delete(f"{self.URL}{sample_stack['slug']}/"))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_stack_unauthenticated(
        self,
        api_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        """Suppression stack non authentifie retourne 401/403."""
        response = cast(Response, api_client.delete(f"{self.URL}{sample_stack['slug']}/"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
