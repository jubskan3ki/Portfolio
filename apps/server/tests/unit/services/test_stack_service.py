"""Tests unitaires pour StackService."""

from __future__ import annotations

import pytest

from core.stacks.services.stack import StackService
from tests.factories import StackCategoryFactory, StackFactory


@pytest.mark.django_db
class TestStackServiceGetByCategory:
    """Tests pour StackService.get_by_category."""

    def test_returns_stacks_for_existing_category(self) -> None:
        """Retourne les stacks d'une categorie existante."""
        category = StackCategoryFactory(name="Backend")
        StackFactory(category=category)
        StackFactory(category=category)

        result = StackService.get_by_category("Backend")

        assert result.count() == 2

    def test_returns_empty_for_nonexistent_category(self) -> None:
        """Retourne un queryset vide pour une categorie inexistante."""
        from utils.exceptions.service import NotFoundError

        with pytest.raises(NotFoundError):
            StackService.get_by_category("Inexistante")

    def test_category_lookup_is_case_insensitive(self) -> None:
        """La recherche par categorie est insensible a la casse."""
        category = StackCategoryFactory(name="Frontend")
        StackFactory(category=category)

        result = StackService.get_by_category("frontend")

        assert result.count() == 1


@pytest.mark.django_db
class TestStackServiceGetRelated:
    """Tests pour StackService.get_related."""

    def test_returns_empty_list_when_no_relations(self) -> None:
        """Retourne une liste vide si pas de relations."""
        stack = StackFactory()

        result = StackService.get_related(stack)

        assert result == []

    def test_returns_related_stacks(self) -> None:
        """Retourne les stacks lies."""
        from core.stacks.models import StackRelationship

        stack_a = StackFactory(name="React")
        stack_b = StackFactory(name="TypeScript")
        StackRelationship.objects.create(
            from_stack=stack_a,
            to_stack=stack_b,
            relationship_type="uses",
        )

        result = StackService.get_related(stack_a)

        assert len(result) >= 1
        names = [r["name"] for r in result]
        assert "TypeScript" in names


@pytest.mark.django_db
class TestStackServiceCRUD:
    """Tests pour les operations CRUD heritees de BaseService."""

    def test_get_by_slug(self) -> None:
        """Recuperation par slug fonctionne."""
        stack = StackFactory(slug="my-stack")

        result = StackService.get_by_slug("my-stack")

        assert result.id == stack.id

    def test_get_by_id(self) -> None:
        """Recuperation par ID fonctionne."""
        stack = StackFactory()

        result = StackService.get_by_id(stack.id)

        assert result.slug == stack.slug
