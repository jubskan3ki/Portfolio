"""Managers pour le module projects."""

from __future__ import annotations

from django.db import models

from utils.models.mixins import WithItemCountMixin


class ProjectQuerySet(models.QuerySet):
    """QuerySet personnalise pour les projets."""

    def with_related(self) -> ProjectQuerySet:
        """Charge les relations FK."""
        return self.select_related("category", "status")

    def by_category(self, slug: str) -> ProjectQuerySet:
        """Filtre par categorie (slug)."""
        return self.with_related().filter(category__slug=slug)

    def by_status(self, name: str) -> ProjectQuerySet:
        """Filtre par statut (nom)."""
        return self.with_related().filter(status__name__iexact=name)


class ProjectManager(models.Manager.from_queryset(ProjectQuerySet)):
    """Manager pour les projets avec select_related par defaut."""

    def get_queryset(self) -> ProjectQuerySet:
        return super().get_queryset().select_related("category", "status")


class ProjectCategoryManager(WithItemCountMixin, models.Manager):
    """Manager pour les categories de projets."""

    item_count_related_name = "projects"


class ProjectStatusManager(WithItemCountMixin, models.Manager):
    """Manager pour les statuts de projets."""

    item_count_related_name = "projects"
