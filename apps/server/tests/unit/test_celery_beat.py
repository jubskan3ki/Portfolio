"""Verifie la coherence du planning Celery Beat.

Garde-fou contre le bug ou une entree de CELERY_BEAT_SCHEDULE reference un nom
de tache qui n'existe pas : Beat publie alors une tache que le worker rejette
("Received unregistered task"), echec silencieux cote requete (ex: les retries
de webhooks ou les cleanups ne tournent jamais).
"""

import pytest
from django.conf import settings

from config.celery import app


@pytest.fixture(scope="module", autouse=True)
def _import_task_modules():
    """Force l'import des modules de taches pour peupler app.tasks."""
    app.loader.import_default_modules()


def _scheduled_task_names() -> list[str]:
    return [entry["task"] for entry in settings.CELERY_BEAT_SCHEDULE.values()]


@pytest.mark.parametrize("task_name", _scheduled_task_names())
def test_beat_schedule_task_is_registered(task_name: str) -> None:
    """Chaque tache planifiee doit exister dans le registre Celery."""
    assert task_name in app.tasks, (
        f"Tache Beat '{task_name}' absente du registre Celery. "
        "Verifier le name= du @shared_task correspondant."
    )
