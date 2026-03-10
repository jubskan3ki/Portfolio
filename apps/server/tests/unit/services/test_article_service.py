"""Tests unitaires pour ArticleService."""

from __future__ import annotations

import pytest

from core.articles.services.article import ArticleService
from tests.factories import ArticleCategoryFactory, ArticleFactory
from utils.exceptions.service import NotFoundError


@pytest.mark.django_db
class TestArticleServiceCreate:
    """Tests pour ArticleService.create()."""

    def test_creates_article(self) -> None:
        """create() cree un article en base."""
        category = ArticleCategoryFactory()
        article = ArticleService.create(
            {
                "title": "Test Article",
                "excerpt": "Excerpt",
                "category": category,
            }
        )

        assert article.id is not None
        assert article.title == "Test Article"
        assert article.category == category

    def test_auto_sets_published_date(self) -> None:
        """create() definit published_date automatiquement si is_published=True."""
        category = ArticleCategoryFactory()
        article = ArticleService.create(
            {
                "title": "Published Article",
                "excerpt": "Excerpt",
                "category": category,
                "is_published": True,
            }
        )

        assert article.published_date is not None

    def test_no_auto_date_when_unpublished(self) -> None:
        """create() ne definit pas published_date si is_published=False."""
        category = ArticleCategoryFactory()
        article = ArticleService.create(
            {
                "title": "Draft Article",
                "excerpt": "Excerpt",
                "category": category,
                "is_published": False,
            }
        )

        assert article.published_date is None

    def test_creates_with_tags(self) -> None:
        """create() associe les tags par nom."""
        category = ArticleCategoryFactory()
        article = ArticleService.create(
            {
                "title": "Tagged Article",
                "excerpt": "Excerpt",
                "category": category,
                "tags": ["Python", "Django"],
            }
        )

        tag_names = list(article.tags.values_list("name", flat=True))
        assert "Python" in tag_names
        assert "Django" in tag_names


@pytest.mark.django_db
class TestArticleServiceUpdate:
    """Tests pour ArticleService.update()."""

    def test_updates_title(self) -> None:
        """update() modifie le titre."""
        article = ArticleFactory()
        updated = ArticleService.update(article.id, {"title": "New Title"})

        assert updated.title == "New Title"

    def test_auto_sets_published_date_on_publish(self) -> None:
        """update() definit published_date quand on publie pour la premiere fois."""
        article = ArticleFactory(is_published=False, published_date=None)
        updated = ArticleService.update(article.id, {"is_published": True})

        assert updated.published_date is not None


@pytest.mark.django_db
class TestArticleServiceGetBySlug:
    """Tests pour ArticleService.get_by_slug()."""

    def test_finds_published_article(self) -> None:
        """get_by_slug() trouve un article publie."""
        article = ArticleFactory(slug="test-find")
        found = ArticleService.get_by_slug("test-find")

        assert found.id == article.id

    def test_raises_not_found_for_missing_slug(self) -> None:
        """get_by_slug() leve NotFoundError pour un slug inexistant."""
        with pytest.raises(NotFoundError):
            ArticleService.get_by_slug("nonexistent-slug")
