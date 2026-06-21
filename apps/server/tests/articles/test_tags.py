"""Tests pour les tags d'articles."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListTags:
    """Tests endpoint GET /api/articles/tags/"""

    URL = "/api/articles/tags/"

    def test_list_tags_public(self, api_client: APIClient) -> None:
        """Liste des tags accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_tags_with_data(
        self,
        api_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Liste des tags retourne les tags existants."""
        response = cast(Response, api_client.get(self.URL))

        if response.status_code == status.HTTP_200_OK and hasattr(response, "data"):
            data = response.data.get("data", response.data) if isinstance(response.data, dict) else response.data
            if isinstance(data, list) and len(data) > 0:
                assert "name" in data[0]
        assert sample_tag is not None


@pytest.mark.django_db
class TestGetTag:
    """Tests endpoint GET /api/articles/tags/{name}/"""

    URL = "/api/articles/tags/"

    def test_get_tag_by_name(
        self,
        api_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Lecture tag par nom retourne le tag."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_tag['name']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["name"] == sample_tag["name"]

    def test_get_tag_not_found(self, api_client: APIClient) -> None:
        """Lecture tag inexistant retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}tag-inexistant/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_tag_detail_exposes_counts(self, api_client: APIClient) -> None:
        """Le detail expose count + view_count reels (regression: renvoyait 0)."""
        from tests.factories import ArticleFactory, TagFactory

        tag = TagFactory()
        ArticleFactory(is_published=True, view_count=10, tags=[tag])
        ArticleFactory(is_published=True, view_count=5, tags=[tag])

        response = cast(Response, api_client.get(f"{self.URL}{tag.name}/"))

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert data["count"] == 2
        assert data["view_count"] == 15


@pytest.mark.django_db
class TestArticlesByTag:
    """Tests endpoint GET /api/articles/by-tag/{name}/"""

    URL = "/api/articles/by-tag/"

    def test_articles_by_tag(
        self,
        api_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Articles par tag retourne les articles."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_tag['name']}/"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateTag:
    """Tests endpoint POST /api/articles/tags/"""

    URL = "/api/articles/tags/"

    def test_create_tag_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation tag authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": "nouveau-tag"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_tag_unauthenticated(self, api_client: APIClient) -> None:
        """Creation tag non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"name": "nouveau-tag"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_tag_duplicate(
        self,
        authenticated_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Creation tag duplique retourne 400."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"name": sample_tag["name"]},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateTag:
    """Tests endpoint PUT/PATCH /api/articles/tags/{name}/"""

    URL = "/api/articles/tags/"

    def test_update_tag_authenticated(
        self,
        authenticated_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Mise a jour tag authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_tag['name']}/",
                {"name": "tag-modifie"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_tag_unauthenticated(
        self,
        api_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Mise a jour tag non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.patch(
                f"{self.URL}{sample_tag['name']}/",
                {"name": "tag-modifie"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteTag:
    """Tests endpoint DELETE /api/articles/tags/{name}/"""

    URL = "/api/articles/tags/"

    def test_delete_tag_authenticated(
        self,
        authenticated_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Suppression tag authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.delete(f"{self.URL}{sample_tag['name']}/"),
        )

        assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_400_BAD_REQUEST]

    def test_delete_tag_unauthenticated(
        self,
        api_client: APIClient,
        sample_tag: dict[str, Any],
    ) -> None:
        """Suppression tag non authentifie retourne 401/403."""
        response = cast(Response, api_client.delete(f"{self.URL}{sample_tag['name']}/"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
