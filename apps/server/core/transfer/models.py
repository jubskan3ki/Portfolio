"""Modeles pour le suivi des operations d'import/export."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.db.models import F

from .managers import ExportJobManager, ImportJobManager


def export_file_upload_to(instance: ExportJob, filename: str) -> str:
    """Chemin dynamique d'upload des fichiers d'export."""
    return f"exports/{instance.id}/{filename}"


class ExportJob(models.Model):
    """Job d'export de donnees."""

    class Status(models.TextChoices):
        """Statuts possibles d'un job d'export."""

        PENDING = "pending", "En attente"
        PROCESSING = "processing", "En cours"
        COMPLETED = "completed", "Termine"
        FAILED = "failed", "Echoue"

    class Format(models.TextChoices):
        """Formats d'export disponibles."""

        JSON = "json", "JSON"
        CSV = "csv", "CSV"
        XLSX = "xlsx", "Excel"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="export_jobs",
    )
    module = models.CharField(max_length=50)
    format = models.CharField(max_length=10, choices=Format.choices, default=Format.JSON)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    file = models.FileField(upload_to=export_file_upload_to, blank=True, null=True)
    filters = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    records_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    objects: ExportJobManager = ExportJobManager()

    class Meta:
        verbose_name = "Job d'export"
        verbose_name_plural = "Jobs d'export"
        db_table = "data_transfer_export_jobs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
            models.Index(fields=["module"]),
        ]

    def __str__(self) -> str:
        return f"Export {self.module} ({self.format}) - {self.status}"


class ImportJob(models.Model):
    """Job d'import de donnees."""

    class Status(models.TextChoices):
        """Statuts possibles d'un job d'import."""

        PENDING = "pending", "En attente"
        VALIDATING = "validating", "Validation"
        PROCESSING = "processing", "En cours"
        COMPLETED = "completed", "Termine"
        FAILED = "failed", "Echoue"
        PARTIALLY_COMPLETED = "partially_completed", "Partiellement termine"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="import_jobs",
    )
    module = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    original_filename = models.CharField(max_length=255)
    file_format = models.CharField(max_length=10)
    total_records = models.PositiveIntegerField(default=0)
    processed_records = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    errors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    objects: ImportJobManager = ImportJobManager()

    class Meta:
        verbose_name = "Job d'import"
        verbose_name_plural = "Jobs d'import"
        db_table = "data_transfer_import_jobs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
            models.Index(fields=["module"]),
        ]

    def __str__(self) -> str:
        return f"Import {self.module} - {self.status} ({self.success_count}/{self.total_records})"

    MAX_STORED_ERRORS = 500

    def add_error(self, row: int, field: str, message: str) -> None:
        """Accumule une erreur en memoire. Appeler flush_errors() pour persister.

        Les erreurs sont plafonnees a MAX_STORED_ERRORS dans la liste JSON
        pour eviter l'explosion memoire. error_count reflete le total reel.
        """
        errors_list: list = self.errors if isinstance(self.errors, list) else []
        self.error_count += 1
        if len(errors_list) < self.MAX_STORED_ERRORS:
            errors_list.append({"row": row, "field": field, "message": message})
        elif len(errors_list) == self.MAX_STORED_ERRORS:
            errors_list.append(
                {
                    "row": 0,
                    "field": "_truncated",
                    "message": f"Trop d'erreurs — seules les {self.MAX_STORED_ERRORS} premieres sont affichees.",
                }
            )
        self.errors = errors_list

    def flush_errors(self) -> None:
        """Persiste les erreurs accumulees en un seul write DB."""
        self.save(update_fields=["errors", "error_count"])

    def increment_success(self) -> None:
        """Incremente le compteur de succes."""

        ImportJob.objects.filter(pk=self.pk).update(
            success_count=F("success_count") + 1,
            processed_records=F("processed_records") + 1,
        )
