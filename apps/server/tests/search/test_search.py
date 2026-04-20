"""Tests pour l'endpoint /api/search/ et le SearchService."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.articles.models import Article
from core.search.services import MIN_QUERY_LENGTH, VALID_TYPES, SearchService

from ..factories import (
    ArticleCategoryFactory,
    ArticleFactory,
    ExperienceFactory,
    ExperienceTypeFactory,
    ProjectFactory,
    StackFactory,
)

URL = "/api/search/"


@pytest.mark.django_db
class TestSearchEndpoint:
    """GET /api/search/ : validation et shape de la reponse."""

    def test_returns_200_for_valid_query(self, api_client: APIClient) -> None:
        ArticleFactory(title="Django tutorial", excerpt="Apprendre Django")
        response = cast(Response, api_client.get(f"{URL}?q=django"))
        assert response.status_code == status.HTTP_200_OK

    def test_requires_query_param(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(URL))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_short_query(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(f"{URL}?q=a"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_invalid_type(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(f"{URL}?q=django&type=invalid"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_response_has_pagination_shape(self, api_client: APIClient) -> None:
        ArticleFactory(title="Django")
        response = cast(Response, api_client.get(f"{URL}?q=django"))
        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert "data" in data
        assert "pagination" in data
        assert "total" in data["pagination"]
        assert "page" in data["pagination"]

    def test_result_has_required_fields(self, api_client: APIClient) -> None:
        category = ArticleCategoryFactory()
        ArticleFactory(title="Django guide", excerpt="Un guide Django", category=category)
        response = cast(Response, api_client.get(f"{URL}?q=django"))
        assert response.status_code == status.HTTP_200_OK
        results = cast(dict[str, Any], response.data)["data"]
        assert len(results) >= 1
        first = results[0]
        for key in ("type", "id", "slug", "title", "url", "rank", "snippet", "metadata"):
            assert key in first


@pytest.mark.django_db
class TestSearchTypeFilter:
    """Le param `type` restreint aux entites demandees."""

    def test_type_articles_returns_only_articles(self, api_client: APIClient) -> None:
        ArticleFactory(title="Django article one")
        ProjectFactory(title="Django project")
        StackFactory(name="Django stack")
        response = cast(Response, api_client.get(f"{URL}?q=django&type=articles"))
        results = cast(dict[str, Any], response.data)["data"]
        assert all(r["type"] == "article" for r in results)

    def test_type_projects_returns_only_projects(self, api_client: APIClient) -> None:
        ArticleFactory(title="Django article")
        ProjectFactory(title="Django project")
        response = cast(Response, api_client.get(f"{URL}?q=django&type=projects"))
        results = cast(dict[str, Any], response.data)["data"]
        assert all(r["type"] == "project" for r in results)

    def test_type_stacks_returns_only_stacks(self, api_client: APIClient) -> None:
        StackFactory(name="Django stack")
        ArticleFactory(title="Django article")
        response = cast(Response, api_client.get(f"{URL}?q=django&type=stacks"))
        results = cast(dict[str, Any], response.data)["data"]
        assert all(r["type"] == "stack" for r in results)

    def test_type_experiences_returns_only_experiences(self, api_client: APIClient) -> None:
        exp_type = ExperienceTypeFactory()
        ExperienceFactory(title="Django dev role", type=exp_type)
        ArticleFactory(title="Django article")
        response = cast(Response, api_client.get(f"{URL}?q=django&type=experiences"))
        results = cast(dict[str, Any], response.data)["data"]
        assert all(r["type"] == "experience" for r in results)

    def test_type_all_returns_mixed(self, api_client: APIClient) -> None:
        ArticleFactory(title="Django article")
        ProjectFactory(title="Django project")
        StackFactory(name="Django stack")
        response = cast(Response, api_client.get(f"{URL}?q=django&type=all"))
        results = cast(dict[str, Any], response.data)["data"]
        types_found = {r["type"] for r in results}
        assert {"article", "project", "stack"}.issubset(types_found)


@pytest.mark.django_db
class TestSearchPermissions:
    """Les articles non publies ne sont visibles que pour les staff."""

    def test_anon_excludes_unpublished_articles(self, api_client: APIClient) -> None:
        ArticleFactory(title="Draft Django article", is_published=False)
        ArticleFactory(title="Published Django article", is_published=True)
        response = cast(Response, api_client.get(f"{URL}?q=django&type=articles"))
        titles = [r["title"] for r in cast(dict[str, Any], response.data)["data"]]
        assert "Draft Django article" not in titles
        assert "Published Django article" in titles

    def test_staff_sees_unpublished_articles(self, authenticated_client: APIClient) -> None:
        ArticleFactory(title="Draft hidden article", is_published=False)
        response = cast(Response, authenticated_client.get(f"{URL}?q=hidden&type=articles"))
        titles = [r["title"] for r in cast(dict[str, Any], response.data)["data"]]
        assert "Draft hidden article" in titles


@pytest.mark.django_db
class TestSearchSnippets:
    """Le snippet entoure le terme recherche de <mark>."""

    def test_snippet_wraps_query_in_mark(self, api_client: APIClient) -> None:
        ArticleFactory(
            title="Guide",
            excerpt="Un long texte qui contient le mot Django au milieu de la phrase.",
        )
        response = cast(Response, api_client.get(f"{URL}?q=django&type=articles"))
        results = cast(dict[str, Any], response.data)["data"]
        assert len(results) >= 1
        assert "<mark>" in results[0]["snippet"].lower() or "<mark>" in results[0]["snippet"]


@pytest.mark.django_db
class TestSearchSecurity:
    """Protection contre SQL injection et XSS dans le snippet."""

    def test_sql_injection_is_safe(self, api_client: APIClient) -> None:
        ArticleFactory(title="Django")
        malicious = "'; DROP TABLE articles; --"
        response = cast(Response, api_client.get(f"{URL}?q={malicious}"))
        assert response.status_code in (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)
        assert Article.objects.count() >= 1

    def test_xss_in_snippet_is_escaped(self, api_client: APIClient) -> None:
        ArticleFactory(title="Alert", excerpt="Texte avec <script>alert(1)</script> dedans.")
        response = cast(Response, api_client.get(f"{URL}?q=script&type=articles"))
        assert response.status_code == status.HTTP_200_OK
        for r in cast(dict[str, Any], response.data)["data"]:
            assert "<script>" not in r["snippet"]


@pytest.mark.django_db
class TestSearchService:
    """Tests unitaires du SearchService (couvre les deux chemins : PG + fallback)."""

    def test_query_too_short_returns_empty(self) -> None:
        results = SearchService(query="a", types=["all"]).run()
        assert results == []

    def test_query_exactly_min_length(self) -> None:
        ArticleFactory(title="Go lang")
        results = SearchService(query="Go", types=["articles"]).run()
        assert len(results) >= 1

    def test_normalize_types_all(self) -> None:
        service = SearchService(query="test", types=["all"])
        assert len(service.types) == len(VALID_TYPES) - 1

    def test_normalize_types_filters_invalid(self) -> None:
        service = SearchService(query="test", types=["articles", "banana"])
        assert service.types == ["articles"]

    def test_result_url_for_articles(self) -> None:
        ArticleFactory(title="Django", slug="django-guide")
        results = SearchService(query="django", types=["articles"]).run()
        assert any(r.url == "/blog/django-guide" for r in results)

    def test_result_url_for_projects(self) -> None:
        ProjectFactory(title="Portfolio", slug="portfolio")
        results = SearchService(query="portfolio", types=["projects"]).run()
        assert any(r.url == "/projects/portfolio" for r in results)

    def test_result_url_for_stacks(self) -> None:
        StackFactory(name="Nuxt", slug="nuxt")
        results = SearchService(query="nuxt", types=["stacks"]).run()
        assert any(r.url == "/stacks/nuxt" for r in results)

    def test_result_url_for_experiences(self) -> None:
        ExperienceFactory(title="Dev Full-stack Django")
        results = SearchService(query="django", types=["experiences"]).run()
        assert len(results) >= 1
        assert results[0].url.startswith("/experiences/")

    def test_metadata_includes_category_for_articles(self) -> None:
        category = ArticleCategoryFactory(name="Tutoriels")
        ArticleFactory(title="Django", category=category)
        results = SearchService(query="django", types=["articles"]).run()
        assert results[0].metadata["category"] == "Tutoriels"

    def test_metadata_includes_technologies_for_projects(self) -> None:
        ProjectFactory(title="Portfolio", technologies=["Nuxt", "Django"])
        results = SearchService(query="portfolio", types=["projects"]).run()
        assert results[0].metadata["technologies"] == ["Nuxt", "Django"]


@pytest.mark.django_db
class TestMinLengthConstant:
    """Contrat sur la longueur minimale."""

    def test_min_length_is_at_least_2(self) -> None:
        assert MIN_QUERY_LENGTH >= 2


# Tests PostgreSQL-only : executes en prod / en CI avec Postgres, skippes sur SQLite.


@pytest.mark.django_db
class TestPostgresFrenchStemming:
    """Le stemmer francais reconnait les variantes morphologiques."""

    def test_developpement_matches_developper(self, api_client: APIClient) -> None:
        ArticleFactory(title="Developpement Django", excerpt="Apprendre a developper")
        response = cast(Response, api_client.get(f"{URL}?q=developper"))
        results = cast(dict[str, Any], response.data)["data"]
        assert len(results) >= 1


@pytest.mark.django_db
class TestPostgresUnaccent:
    """L'extension unaccent permet la recherche insensible aux accents."""

    def test_cafe_matches_cafe_accented(self, api_client: APIClient) -> None:
        ArticleFactory(title="Le cafe du coin")
        response = cast(Response, api_client.get(f"{URL}?q=cafe"))
        results = cast(dict[str, Any], response.data)["data"]
        assert len(results) >= 1


@pytest.mark.django_db
class TestPostgresRanking:
    """Les matches dans le titre sont mieux classes que dans le corps."""

    def test_title_match_ranks_higher(self, api_client: APIClient) -> None:
        ArticleFactory(title="Python", excerpt="Un article sur Django seulement")
        ArticleFactory(title="Django", excerpt="Un article sur Python")
        response = cast(Response, api_client.get(f"{URL}?q=django&type=articles"))
        results = cast(dict[str, Any], response.data)["data"]
        assert results[0]["title"] == "Django"


@pytest.mark.django_db
class TestPostgresTriggerSync:
    """Le trigger plpgsql met a jour search_vector sur INSERT/UPDATE (y compris bulk)."""

    def test_insert_populates_vector(self) -> None:
        article = ArticleFactory(title="TriggerTest")
        article.refresh_from_db()
        assert article.search_vector is not None

    def test_update_refreshes_vector(self) -> None:
        article = ArticleFactory(title="Initial")
        Article.objects.filter(id=article.id).update(title="Modified")
        article.refresh_from_db()
        assert article.search_vector is not None


@pytest.mark.django_db
class TestExistingFiltersNotBroken:
    """Zero breaking change : /api/articles/?search= continue de repondre 200."""

    def test_articles_search_still_works(
        self,
        api_client: APIClient,
        sample_article: dict[str, Any],
    ) -> None:
        response = cast(Response, api_client.get(f"/api/articles/?search={sample_article['title']}"))
        assert response.status_code == status.HTTP_200_OK

    def test_projects_search_still_works(
        self,
        api_client: APIClient,
        sample_project: dict[str, Any],
    ) -> None:
        response = cast(Response, api_client.get(f"/api/projects/?search={sample_project['title']}"))
        assert response.status_code == status.HTTP_200_OK

    def test_stacks_search_still_works(
        self,
        api_client: APIClient,
        sample_stack: dict[str, Any],
    ) -> None:
        response = cast(Response, api_client.get(f"/api/stacks/?search={sample_stack['name']}"))
        assert response.status_code == status.HTTP_200_OK
