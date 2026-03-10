"""Managers pour le module audit."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from core.audit.models import AuditLog


class AuditLogManager(models.Manager["AuditLog"]):
    """Manager pour les logs d'audit."""

    def get_queryset(self) -> models.QuerySet[AuditLog]:
        """QuerySet par defaut avec select_related."""
        return super().get_queryset().select_related("user")

    def for_model(self, model_name: str) -> models.QuerySet[AuditLog]:
        """Filtre les logs par nom de modele."""
        return self.get_queryset().filter(model_name=model_name)

    def for_object(self, model_name: str, object_id: str | int) -> models.QuerySet[AuditLog]:
        """Filtre les logs par objet specifique."""
        return self.get_queryset().filter(model_name=model_name, object_id=str(object_id))

    def by_user(self, user_id: int) -> models.QuerySet[AuditLog]:
        """Filtre les logs par utilisateur."""
        return self.get_queryset().filter(user_id=user_id)

    def recent(self, limit: int = 50) -> models.QuerySet[AuditLog]:
        """Retourne les logs les plus recents."""
        return self.get_queryset().order_by("-timestamp")[:limit]
