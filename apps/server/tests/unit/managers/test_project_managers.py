"""Tests unitaires pour les managers de projets."""

from __future__ import annotations

import pytest

from core.projects.models import Project
from tests.factories import ProjectCategoryFactory, ProjectFactory, ProjectStatusFactory


@pytest.mark.django_db
class TestProjectQuerySet:
    """Tests pour ProjectQuerySet."""

    def test_by_category_filters_correctly(self) -> None:
        """Filtre par categorie (slug) correctement."""
        cat_web = ProjectCategoryFactory(slug="web")
        cat_mobile = ProjectCategoryFactory(slug="mobile")
        ProjectFactory(category=cat_web)
        ProjectFactory(category=cat_mobile)

        result = Project.objects.by_category("web")

        assert result.count() == 1

    def test_by_status_filters_correctly(self) -> None:
        """Filtre par statut correctement."""
        status_active = ProjectStatusFactory(name="Active")
        status_archived = ProjectStatusFactory(name="Archived")
        ProjectFactory(status=status_active)
        ProjectFactory(status=status_archived)

        result = Project.objects.by_status("Active")

        assert result.count() == 1

    def test_by_status_case_insensitive(self) -> None:
        """Le filtre par statut est insensible a la casse."""
        status_obj = ProjectStatusFactory(name="Completed")
        ProjectFactory(status=status_obj)

        result = Project.objects.by_status("completed")

        assert result.count() == 1

    def test_with_related_loads_relations(self) -> None:
        """with_related charge les relations FK."""
        category = ProjectCategoryFactory()
        ProjectFactory(category=category)

        project = Project.objects.with_related().first()

        assert project.category is not None
