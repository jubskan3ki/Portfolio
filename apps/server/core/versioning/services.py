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


class UnsupportedModelError(Exception):
    """Leve quand un modele ne supporte pas le soft-delete (pas de all_objects)."""


class ObjectNotFoundError(Exception):
    """Leve quand l'objet cible d'une operation est introuvable."""


def _resolve_model(model_name: str):
    """Retourne la classe du modele depuis son nom simple (ex: 'Article')."""
    for model in apps.get_models():
        if model.__name__ == model_name:
            return model
    raise UnknownModelError(f"Model '{model_name}' introuvable.")


def list_versions(model_name: str, object_id: str) -> Any:
    """Retourne les versions d'un objet, triees par numero decroissant.

    Filtre l'historique sur le nom du content_type sans resoudre le modele
    (comportement historique : aucune validation d'existence du modele ici).
    """
    return (
        Version.objects.select_related("created_by")
        .filter(content_type=model_name, object_id=object_id)
        .order_by("-version_number")
    )


def list_trashed(model_name: str) -> list[dict[str, Any]]:
    """Retourne les objets soft-deleted d'un modele.

    Leve UnknownModelError si le modele est introuvable et UnsupportedModelError
    s'il ne supporte pas le soft-delete.
    """
    model = _resolve_model(model_name)
    if not hasattr(model, "all_objects"):
        raise UnsupportedModelError(f"Modele {model_name} ne supporte pas le soft-delete.")
    trashed = model.all_objects.filter(deleted_at__isnull=False).values("pk", "deleted_at", "deleted_by_id")
    return list(trashed)


def untrash(model_name: str, object_id: str) -> Any:
    """Restaure un objet soft-deleted et retourne l'instance.

    Leve UnknownModelError / UnsupportedModelError pour les modeles invalides
    et ObjectNotFoundError si l'objet est introuvable.
    """
    model = _resolve_model(model_name)
    if not hasattr(model, "all_objects"):
        raise UnsupportedModelError(f"Modele {model_name} ne supporte pas le soft-delete.")
    try:
        instance = model.all_objects.get(pk=object_id)
    except model.DoesNotExist as exc:
        raise ObjectNotFoundError("Objet introuvable.") from exc
    instance.restore()
    return instance


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
    # select_for_update : verrouille la ligne cible le temps du restore pour
    # qu'un restore concurrent (ou une edition normale simultanee) ne provoque
    # pas de lost update (le dernier save ecraserait l'autre en silence).
    instance = qs.select_for_update().get(pk=version.object_id)

    snapshot = version.snapshot or {}
    for field in instance._meta.fields:
        name = field.name
        if name == "id" or name not in snapshot:
            continue
        setattr(instance, field.attname, snapshot[name])

    instance.save()
    return instance
