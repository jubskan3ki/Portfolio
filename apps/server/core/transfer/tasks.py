"""Taches Celery pour le module Transfer."""

import logging
from datetime import timedelta
from io import BytesIO

from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import DatabaseError, OperationalError, transaction
from django.utils import timezone

from .models import ExportJob, ImportJob
from .services import ExporterService, ImporterService

logger = logging.getLogger("core.transfer")


@shared_task(name="data_transfer.cleanup_old_jobs")
def cleanup_old_jobs(days: int = 30) -> dict:
    """Supprime les anciens jobs d'import/export.

    Args:
        days: Nombre de jours a conserver

    Returns:
        Dict avec le nombre de jobs supprimes
    """
    cutoff = timezone.now() - timedelta(days=days)

    # Suppression atomique : fichiers + entrées DB dans la même transaction
    old_exports = ExportJob.objects.filter(created_at__lt=cutoff)
    export_count = old_exports.count()

    with transaction.atomic():
        for job in old_exports:
            if job.file:
                try:
                    job.file.delete(save=False)
                except (OSError, ValueError):
                    logger.exception("Erreur suppression fichier export job %s", job.id)
        old_exports.delete()

    import_count, _ = ImportJob.objects.filter(created_at__lt=cutoff).delete()

    logger.info("Cleanup: %d exports et %d imports supprimes", export_count, import_count)

    return {
        "exports_deleted": export_count,
        "imports_deleted": import_count,
    }


@shared_task(
    name="data_transfer.async_export",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(DatabaseError, OperationalError),
)
def async_export(_self, job_id: str) -> dict:
    """Execute un export de maniere asynchrone.

    Args:
        job_id: ID du job d'export

    Returns:
        Dict avec le statut du job
    """
    try:
        job = ExportJob.objects.get(id=job_id)
    except ExportJob.DoesNotExist:
        logger.exception("Job d'export non trouve: %s", job_id)
        return {"error": "Job non trouve"}

    if job.status != ExportJob.Status.PENDING:
        return {"status": job.status, "message": "Job deja traite"}

    job = ExporterService.run_export(job)

    return {
        "job_id": str(job.id),
        "status": job.status,
        "records_count": job.records_count,
    }


@shared_task(
    name="data_transfer.async_import",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(DatabaseError, OperationalError),
)
def async_import(_self, job_id: str, file_content: bytes, *, update_existing: bool = False) -> dict:
    """Execute un import de maniere asynchrone.

    Args:
        job_id: ID du job d'import
        file_content: Contenu du fichier
        update_existing: Mettre a jour les enregistrements existants

    Returns:
        Dict avec le statut du job
    """
    try:
        job = ImportJob.objects.get(id=job_id)
    except ImportJob.DoesNotExist:
        logger.exception("Job d'import non trouve: %s", job_id)
        return {"error": "Job non trouve"}

    if job.status != ImportJob.Status.PENDING:
        return {"status": job.status, "message": "Job deja traite"}

    try:
        file_io = BytesIO(file_content)
        file = InMemoryUploadedFile(
            file=file_io,
            field_name="file",
            name=job.original_filename,
            content_type="application/octet-stream",
            size=len(file_content),
            charset=None,
        )

        job = ImporterService.execute_import(
            job=job,
            file=file,
            update_existing=update_existing,
        )

        return {
            "job_id": str(job.id),
            "status": job.status,
            "success_count": job.success_count,
            "error_count": job.error_count,
        }

    except (DatabaseError, OperationalError, ValueError) as e:
        logger.exception("Erreur lors de l'import asynchrone")
        job.status = ImportJob.Status.FAILED
        if not job.errors:
            job.errors = []
        job.errors.append({"row": 0, "field": "system", "message": str(e)})
        job.save()

        return {
            "job_id": str(job.id),
            "status": job.status,
            "error": str(e),
        }
