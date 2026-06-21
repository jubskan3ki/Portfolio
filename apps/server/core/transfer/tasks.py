"""Taches Celery pour le module Transfer."""

import logging
from datetime import timedelta

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import ExportJob, ImportJob

logger = logging.getLogger("core.transfer")


def _delete_files(files: list) -> None:
    """Supprime les fichiers du stockage (appele en on_commit, hors transaction)."""
    for file in files:
        try:
            file.delete(save=False)
        except (OSError, ValueError):
            logger.exception("Erreur suppression fichier export: %s", getattr(file, "name", "?"))


@shared_task(name="data_transfer.cleanup_old_jobs")
def cleanup_old_jobs(days: int = 30) -> dict:
    """Supprime les anciens jobs d'import/export (anterieurs a `days` jours)."""
    from utils.locks import single_run_lock

    with single_run_lock("data_transfer.cleanup_old_jobs", 3600) as acquired:
        if not acquired:
            logger.info("Cleanup jobs deja en cours, run ignore")
            return {"exports_deleted": 0, "imports_deleted": 0, "skipped": True}

        cutoff = timezone.now() - timedelta(days=days)

        old_exports = ExportJob.objects.filter(created_at__lt=cutoff)
        export_count = old_exports.count()

        # Capturer les fichiers avant delete() mais ne les effacer qu'apres COMMIT : un rollback laisserait sinon des lignes DB pointant vers des fichiers deja supprimes.
        files_to_delete = [job.file for job in old_exports if job.file]

        with transaction.atomic():
            old_exports.delete()
            transaction.on_commit(lambda: _delete_files(files_to_delete))

        import_count, _ = ImportJob.objects.filter(created_at__lt=cutoff).delete()

        logger.info("Cleanup: %d exports et %d imports supprimes", export_count, import_count)

        return {
            "exports_deleted": export_count,
            "imports_deleted": import_count,
        }
