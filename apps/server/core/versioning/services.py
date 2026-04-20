"""Services versioning : restore d'une version ancienne."""

from __future__ import annotations

from typing import Any

from django.apps import apps
from django.db import transaction

from core.versioning.models import Version


class VersionNotFoundError(Exception):
    """Leve quand la version demandee n'existe pas."""


class UnknownModelError(Exception):
    """Leve quand le content_type pointe vers un modele introuvable."""


def _resolve_model(model_name: str):
    """Retourne la classe du modele depuis son nom simple (ex: 'Article')."""
    for model in apps.get_models():
        if model.__name__ == model_name:
            return model
    raise UnknownModelError(f"Model '{model_name}' introuvable.")


@transaction.atomic
def restore_version(version_id: int, user: Any = None) -> Any:
    """Restaure un objet a l'etat d'une version donnee.

    Retourne l'instance mise a jour. Cree une nouvelle Version apres le restore
    (via le signal post_save), garantissant une chaine continue d'historique.
    """
    del user
    try:
        version = Version.objects.get(pk=version_id)
    except Version.DoesNotExist as exc:
        raise VersionNotFoundError(f"Version {version_id} introuvable.") from exc

    model = _resolve_model(version.content_type)
    qs = getattr(model, "all_objects", model.objects)
    instance = qs.get(pk=version.object_id)

    snapshot = version.snapshot or {}
    for field in instance._meta.fields:
        name = field.name
        if name == "id" or name not in snapshot:
            continue
        setattr(instance, field.attname, snapshot[name])

    instance.save()
    return instance
