"""Modele Version : snapshot polymorphique + SoftDeleteMixin reutilisable."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet qui filtre les objets supprimes."""

    def alive(self) -> QuerySet:
        return self.filter(deleted_at__isnull=True)

    def trashed(self) -> QuerySet:
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Manager par defaut qui exclut les objets supprimes.

    Pour acceder aux soft-deleted, utiliser `all_objects` sur le modele.
    """

    def get_queryset(self) -> QuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class SoftDeleteAllManager(models.Manager):
    """Manager qui retourne tous les objets, y compris soft-deleted."""

    def get_queryset(self) -> QuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteMixin(models.Model):
    """Mixin abstrait ajoutant soft-delete.

    Les sous-classes doivent declarer `objects = SoftDeleteManager()` et
    `all_objects = SoftDeleteAllManager()` pour garder la compat avec les
    queries existantes (un modele peut garder son manager custom tant qu'il
    derive de SoftDeleteManager).
    """

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True

    def soft_delete(self, user: Any = None) -> None:
        """Marque l'objet comme supprime sans detruire la ligne."""
        self.deleted_at = timezone.now()
        self.deleted_by = user if (user and getattr(user, "is_authenticated", False)) else None
        self.save(update_fields=["deleted_at", "deleted_by"])

    def restore(self) -> None:
        """Annule la suppression soft."""
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["deleted_at", "deleted_by"])


class Version(models.Model):
    """Snapshot polymorphique d'un modele a un instant donne.

    Stockage : content_type + object_id + version_number (unique par objet) + snapshot JSON.
    """

    content_type = models.CharField(max_length=100, db_index=True, help_text="model_name de l'objet")
    object_id = models.CharField(max_length=100, db_index=True)
    version_number = models.PositiveIntegerField()
    snapshot = models.JSONField(default=dict, help_text="Etat complet de l'objet au moment de cette version")
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        db_table = "versioning_versions"
        ordering = ["-version_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "version_number"],
                name="unique_version_per_object",
            ),
        ]
        indexes = [
            models.Index(fields=["content_type", "object_id", "-version_number"]),
        ]

    def __str__(self) -> str:
        return f"{self.content_type}:{self.object_id} v{self.version_number}"
