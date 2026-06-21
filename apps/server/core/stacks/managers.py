"""Managers pour le module stacks."""

from __future__ import annotations

from django.db import models

from utils.models.mixins import WithItemCountMixin


class StackQuerySet(models.QuerySet):
    """QuerySet personnalise pour les stacks."""

    def with_related(self) -> StackQuerySet:
        """Charge la categorie (FK) pour les listes."""
        return self.select_related("category")

    def with_detail(self) -> StackQuerySet:
        """Charge la categorie + prefetch ressources et relations pour le detail.

        Source unique du prefetch des relations, reutilisee par le ViewSet (retrieve)
        et par StackService._get_detail_queryset.
        """
        from .models import StackRelationship

        return self.select_related("category").prefetch_related(
            "resources",
            models.Prefetch(
                "relationships",
                queryset=StackRelationship.objects.select_related("to_stack", "to_stack__category"),
            ),
        )

    def by_category(self, slug_or_name: str) -> StackQuerySet:
        """Filtre par categorie."""
        return self.with_related().filter(models.Q(category__name__iexact=slug_or_name))

    def featured(self) -> StackQuerySet:
        """Stacks avec le plus haut niveau."""
        return self.with_related().order_by("-level")


StackManager = models.Manager.from_queryset(StackQuerySet)


class StackCategoryManager(WithItemCountMixin, models.Manager):
    """Manager pour les categories de stacks."""

    item_count_related_name = "stacks"


class StackRelationshipManager(models.Manager):
    """Manager pour les relations entre stacks."""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("from_stack", "to_stack")


class StackResourceManager(models.Manager):
    """Manager pour les ressources de stacks."""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("stack")
