"""Managers pour le module experiences."""

from __future__ import annotations

from django.db import models

from utils.models.mixins import WithItemCountMixin


class ExperienceQuerySet(models.QuerySet):
    """QuerySet personnalise pour les experiences."""

    def with_related(self) -> ExperienceQuerySet:
        """Charge les relations FK."""
        return self.select_related("type")

    def current(self) -> ExperienceQuerySet:
        """Experiences en cours (sans date de fin)."""
        return self.with_related().filter(end_date__isnull=True)

    def by_type(self, type_name: str) -> ExperienceQuerySet:
        """Filtre par type d'experience."""
        return self.with_related().filter(type__name__iexact=type_name)


class ExperienceManager(models.Manager):
    """Manager pour les experiences avec select_related par defaut."""

    def get_queryset(self) -> ExperienceQuerySet:
        return ExperienceQuerySet(self.model, using=self._db).select_related("type")

    def with_related(self) -> ExperienceQuerySet:
        return self.get_queryset().with_related()

    def current(self) -> ExperienceQuerySet:
        return self.get_queryset().current()

    def by_type(self, type_name: str) -> ExperienceQuerySet:
        return self.get_queryset().by_type(type_name)


class ExperienceTypeManager(WithItemCountMixin, models.Manager):
    """Manager pour les types d'experiences."""

    item_count_related_name = "experiences"
