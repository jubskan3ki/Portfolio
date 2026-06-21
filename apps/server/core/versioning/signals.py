"""Signaux qui capturent un snapshot Version avant chaque save des modeles enregistres."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from django.db import connection, transaction
from django.db.models import Model
from django.db.models.signals import post_save

if TYPE_CHECKING:
    from core.user.models import User as AppUser

from core.audit.signals import IGNORED_FIELDS, _serialize_value, get_audit_context
from core.versioning.models import Version

logger = logging.getLogger(__name__)

VERSIONED_MODELS: set[str] = {"Article"}


def _should_version(instance: Model) -> bool:
    from utils.signals import bulk_mode_active

    # Import en masse : snapshot par-objet desactive (cf. utils.signals).
    if bulk_mode_active():
        return False
    return instance.__class__.__name__ in VERSIONED_MODELS


def _build_snapshot(instance: Model) -> dict[str, Any]:
    snapshot: dict[str, Any] = {}
    for field in instance._meta.fields:
        name = field.name
        if name in IGNORED_FIELDS:
            continue
        value = getattr(instance, name, None)
        if hasattr(field, "remote_field") and field.remote_field:
            value = getattr(value, "pk", None) if value else None
        snapshot[name] = _serialize_value(value)
    return snapshot


def _next_version_number(model_name: str, object_id: str) -> int:
    last = Version.objects.filter(content_type=model_name, object_id=object_id).order_by("-version_number").first()
    return (last.version_number + 1) if last else 1


def _snapshot(sender, instance: Model, created, **kwargs) -> None:
    del sender, created, kwargs
    if not _should_version(instance):
        return
    try:
        model_name = instance.__class__.__name__
        object_id = str(instance.pk)
        context = get_audit_context()
        # Verrou consultatif par objet : serialise la creation de snapshots
        # concurrents pour le meme objet. Sinon deux saves simultanes calculent
        # le meme version_number (MAX+1), et le 2e create viole la contrainte
        # unique (content_type, object_id, version_number) -> IntegrityError
        # avale par le except, donc snapshot d'historique silencieusement perdu.
        # atomic imbrique = savepoint : reste fail-open pour la transaction metier.
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_advisory_xact_lock(hashtext(%s))",
                    [f"version:{model_name}:{object_id}"],
                )
            Version.objects.create(
                content_type=model_name,
                object_id=object_id,
                version_number=_next_version_number(model_name, object_id),
                snapshot=_build_snapshot(instance),
                created_by=cast("AppUser | None", context["user"]),
            )
    except Exception:
        logger.exception("Failed to create version snapshot for %s", instance)


post_save.connect(_snapshot, dispatch_uid="versioning_post_save")
