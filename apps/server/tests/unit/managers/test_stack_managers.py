"""Tests unitaires pour les managers de stacks."""

from __future__ import annotations

import pytest

from core.stacks.models import Stack
from tests.factories import StackCategoryFactory, StackFactory


@pytest.mark.django_db
class TestStackQuerySet:
    """Tests pour StackQuerySet."""

    def test_by_category_filters_correctly(self) -> None:
        """Filtre par categorie correctement."""
        cat_backend = StackCategoryFactory(name="Backend")
        cat_frontend = StackCategoryFactory(name="Frontend")
        StackFactory(category=cat_backend)
        StackFactory(category=cat_frontend)

        result = Stack.objects.by_category("Backend")

        assert result.count() == 1
        assert result.first().category.name == "Backend"

    def test_by_category_case_insensitive(self) -> None:
        """Le filtre par categorie est insensible a la casse."""
        category = StackCategoryFactory(name="DevOps")
        StackFactory(category=category)

        result = Stack.objects.by_category("devops")

        assert result.count() == 1

    def test_featured_orders_by_level(self) -> None:
        """Featured retourne les stacks tries par niveau decroissant."""
        category = StackCategoryFactory()
        StackFactory(category=category, level=50)
        StackFactory(category=category, level=90)
        StackFactory(category=category, level=70)

        result = list(Stack.objects.featured())

        assert result[0].level >= result[1].level >= result[2].level

    def test_with_related_loads_relations(self) -> None:
        """with_related charge les relations FK."""
        category = StackCategoryFactory()
        StackFactory(category=category)

        stack = Stack.objects.with_related().first()

        # Should not raise | related fields are prefetched
        assert stack.category is not None
