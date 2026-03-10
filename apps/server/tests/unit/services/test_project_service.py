"""Tests unitaires pour ProjectService."""

from __future__ import annotations

import pytest

from core.projects.services.project import ProjectService
from tests.factories import ProjectCategoryFactory, ProjectFactory


@pytest.mark.django_db
class TestProjectServiceGetByCategory:
    """Tests pour ProjectService.get_by_category."""

    def test_returns_projects_for_existing_category(self) -> None:
        """Retourne les projets d'une categorie existante."""
        category = ProjectCategoryFactory(slug="web")
        ProjectFactory(category=category)
        ProjectFactory(category=category)

        result = ProjectService.get_by_category("web")

        assert result.count() == 2

    def test_returns_empty_for_nonexistent_category(self) -> None:
        """Retourne un queryset vide pour une categorie inexistante."""
        result = ProjectService.get_by_category("inexistant")

        assert result.count() == 0


@pytest.mark.django_db
class TestProjectServiceGetFeatured:
    """Tests pour ProjectService.get_featured."""

    def test_returns_featured_projects(self) -> None:
        """Retourne les projets featured."""
        ProjectFactory()
        ProjectFactory()

        result = ProjectService.get_featured(limit=5)

        assert result.count() >= 1

    def test_respects_limit(self) -> None:
        """Respecte la limite specifiee."""
        for _ in range(5):
            ProjectFactory()

        result = ProjectService.get_featured(limit=2)

        assert result.count() == 2


@pytest.mark.django_db
class TestProjectServiceCRUD:
    """Tests pour les operations CRUD heritees de BaseService."""

    def test_get_by_slug(self) -> None:
        """Recuperation par slug fonctionne."""
        project = ProjectFactory(slug="my-project")

        result = ProjectService.get_by_slug("my-project")

        assert result.id == project.id

    def test_get_by_id(self) -> None:
        """Recuperation par ID fonctionne."""
        project = ProjectFactory()

        result = ProjectService.get_by_id(project.id)

        assert result.slug == project.slug
