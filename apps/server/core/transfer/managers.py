"""Managers pour le module transfer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from core.transfer.models import ExportJob, ImportJob
    from core.user.models import User


class ExportJobManager(models.Manager["ExportJob"]):
    """Manager pour les jobs d'export."""

    def get_queryset(self) -> models.QuerySet[ExportJob]:
        return super().get_queryset().select_related("user")

    def pending(self) -> models.QuerySet[ExportJob]:
        """Jobs en attente."""
        return self.get_queryset().filter(status="pending")

    def for_user(self, user: User) -> models.QuerySet[ExportJob]:
        """Jobs d'un utilisateur."""
        return self.get_queryset().filter(user=user)


class ImportJobManager(models.Manager["ImportJob"]):
    """Manager pour les jobs d'import."""

    def get_queryset(self) -> models.QuerySet[ImportJob]:
        return super().get_queryset().select_related("user")

    def pending(self) -> models.QuerySet[ImportJob]:
        """Jobs en attente."""
        return self.get_queryset().filter(status="pending")

    def for_user(self, user: User) -> models.QuerySet[ImportJob]:
        """Jobs d'un utilisateur."""
        return self.get_queryset().filter(user=user)
