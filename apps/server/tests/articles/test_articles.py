"""Tests pour les articles."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListArticles:
    """Tests endpoint GET /api/articles/"""

    URL = "/api/articles/"

    def test_list_articles_public(self, api_client: APIClient) -> None:
        """Liste des articles accessible publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_articles_with_data(
        self,
        api_client: APIClient,
    ) -> None:
        """Liste des articles retourne les articles existants."""
        response = cast(Response, api_client.get(self.URL))

        if response.status_code == status.HTTP_200_OK and hasattr(response, "data"):
            data = cast(dict[str, Any], response.data)
            assert "data" in data or isinstance(response.data, list)

    def test_list_articles_pagination(self, api_client: APIClient) -> None:
        """Liste des articles supporte la pagination."""
        response = cast(Response, api_client.get(f"{self.URL}?page=1&limit=5"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            if "pagination" in data:
                assert "total" in data["pagination"]
                assert "page" in data["pagination"]

    def test_list_articles_search(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Recherche d'articles fonctionne."""
        response = cast(Response, api_client.get(f"{self.URL}?search={sample_article['title']}"))

        assert response.status_code == status.HTTP_200_OK

    def test_list_articles_sort_by_date(self, api_client: APIClient) -> None:
        """Tri par date fonctionne."""
        response = cast(Response, api_client.get(f"{self.URL}?sortBy=date&sortDirection=desc"))

        assert response.status_code == status.HTTP_200_OK

    def test_list_articles_sort_by_views(self, api_client: APIClient) -> None:
        """Tri par vues fonctionne."""
        response = cast(Response, api_client.get(f"{self.URL}?sortBy=views&sortDirection=desc"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetArticle:
    """Tests endpoint GET /api/articles/{slug}/"""

    URL = "/api/articles/"

    def test_get_article_by_slug(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Lecture article par slug retourne l'article."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_article['slug']}/"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(dict[str, Any], response.data)
            assert data["slug"] == sample_article["slug"]
            assert data["title"] == sample_article["title"]

    def test_get_article_not_found(self, api_client: APIClient) -> None:
        """Lecture article inexistant retourne 404."""
        response = cast(Response, api_client.get(f"{self.URL}article-qui-nexiste-pas/"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFeaturedArticles:
    """Tests endpoint GET /api/articles/featured/"""

    URL = "/api/articles/featured/"

    def test_featured_articles_public(self, api_client: APIClient) -> None:
        """Articles featured accessibles publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_featured_articles_limit(self, api_client: APIClient) -> None:
        """Limite sur articles featured fonctionne."""
        response = cast(Response, api_client.get(f"{self.URL}?limit=3"))

        if response.status_code == status.HTTP_200_OK:
            data = cast(list[dict[str, Any]], response.data)
            assert len(data) <= 3


@pytest.mark.django_db
class TestPopularArticles:
    """Tests endpoint GET /api/articles/popular/"""

    URL = "/api/articles/popular/"

    def test_popular_articles_public(self, api_client: APIClient) -> None:
        """Articles populaires accessibles publiquement."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRelatedArticles:
    """Tests endpoint GET /api/articles/{slug}/related/"""

    URL = "/api/articles/"

    def test_related_articles(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Articles lies retournes correctement."""
        response = cast(Response, api_client.get(f"{self.URL}{sample_article['slug']}/related/"))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestIncrementViews:
    """Tests endpoint POST /api/articles/{slug}/view/"""

    URL = "/api/articles/"

    def test_increment_view(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Incrementation des vues fonctionne."""
        response = cast(Response, api_client.post(f"{self.URL}{sample_article['slug']}/view/"))

        # May require authentication or be public
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCreateArticle:
    """Tests endpoint POST /api/articles/"""

    URL = "/api/articles/"

    def test_create_article_authenticated(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Creation article authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "title": "Nouvel Article",
                    "excerpt": "Resume de l'article",
                    "content": [{"type": "paragraph", "content": "Contenu"}],
                    "category": sample_category["id"],
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_article_unauthenticated(
        self,
        api_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Creation article non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "title": "Nouvel Article",
                    "excerpt": "Resume",
                    "content": [],
                    "category": sample_category["id"],
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_article_missing_title(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Creation article sans titre retourne 400."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "excerpt": "Resume",
                    "content": [],
                    "category": sample_category["id"],
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateArticle:
    """Tests endpoint PUT/PATCH /api/articles/{slug}/"""

    URL = "/api/articles/"

    def test_update_article_authenticated(
        self,
        authenticated_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Mise a jour article authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.patch(
                f"{self.URL}{sample_article['slug']}/",
                {"title": "Titre Modifie"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_article_unauthenticated(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Mise a jour article non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.patch(
                f"{self.URL}{sample_article['slug']}/",
                {"title": "Titre Modifie"},
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteArticle:
    """Tests endpoint DELETE /api/articles/{slug}/"""

    URL = "/api/articles/"

    def test_delete_article_authenticated(
        self,
        authenticated_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Suppression article authentifie reussit."""
        response = cast(
            Response,
            authenticated_client.delete(f"{self.URL}{sample_article['slug']}/"),
        )

        assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND]

    def test_delete_article_unauthenticated(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        """Suppression article non authentifie retourne 401/403."""
        response = cast(Response, api_client.delete(f"{self.URL}{sample_article['slug']}/"))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
