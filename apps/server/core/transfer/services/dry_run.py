"""Service dry-run : simule un import dans une transaction rollbackee + produit un diff."""

from __future__ import annotations

import logging
from typing import Any

from django.apps import apps
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from core.transfer.services.importer import ImporterService
from core.transfer.services.validators import DataValidator

logger = logging.getLogger("core.transfer")


def _resolve_unique_field(module: str) -> tuple[str, ...]:
    raw = ImporterService.UNIQUE_FIELDS.get(module, "slug")
    return (raw,) if isinstance(raw, str) else raw


def _resolve_model(module: str):
    mapping = {
        "articles": ("articles", "Article"),
        "projects": ("projects", "Project"),
        "stacks": ("stacks", "Stack"),
        "experiences": ("experiences", "Experience"),
    }
    app_label, model_name = mapping[module]
    return apps.get_model(app_label, model_name)


def _preload_existing(model: Any, unique_fields: tuple[str, ...], records: list[dict[str, Any]]) -> dict[tuple, Any]:
    """Pre-charge en une requete les instances existantes correspondant aux records.

    Evite un SELECT par ligne : on collecte les cles uniques completes presentes dans
    le fichier, on filtre en base sur le premier champ unique (borne le resultat) puis
    on indexe par tuple de cle dans l'ordre de `unique_fields`.
    """
    keys = [
        tuple(record.get(f) for f in unique_fields)
        for record in records
        if all(record.get(f) is not None for f in unique_fields)
    ]
    if not keys:
        return {}

    first_field = unique_fields[0]
    first_values = {key[0] for key in keys}
    queryset = model.objects.filter(**{f"{first_field}__in": first_values})
    return {tuple(getattr(obj, f) for f in unique_fields): obj for obj in queryset}


def _compute_diff(existing: Any, new_values: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Pour une instance existante, calcule les champs qui changeraient."""
    diff: dict[str, dict[str, Any]] = {}
    for field, new_value in new_values.items():
        if not hasattr(existing, field):
            continue
        current = getattr(existing, field)
        if current != new_value:
            diff[field] = {"current": _stringify(current), "new": _stringify(new_value)}
    return diff


def _stringify(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool | list | dict):
        return value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def dry_run_import(file: UploadedFile, module: str) -> dict[str, Any]:
    """Parse le fichier et classifie chaque record : creation, update (avec diff), skip, erreur.

    Aucune modification persistee : la transaction est rollbackee a la fin.
    """
    ImporterService.validate_module(module)
    records, file_format = ImporterService.parse_file(file)
    file.seek(0)

    unique_fields = _resolve_unique_field(module)
    model = _resolve_model(module)

    would_create: list[dict[str, Any]] = []
    would_update: list[dict[str, Any]] = []
    would_skip: list[dict[str, Any]] = []
    validation_errors: list[dict[str, Any]] = []

    valid_count, errors = DataValidator.validate_batch(module, records)
    error_by_index = {e.get("index"): e for e in errors if isinstance(e, dict) and "index" in e}

    existing_by_key = _preload_existing(model, unique_fields, records)

    with transaction.atomic():
        sid = transaction.savepoint()
        for idx, record in enumerate(records):
            if idx in error_by_index:
                validation_errors.append({"index": idx, "record": record, "error": error_by_index[idx]})
                continue

            lookup = {f: record.get(f) for f in unique_fields if record.get(f) is not None}
            if not lookup or len(lookup) != len(unique_fields):
                would_skip.append({"index": idx, "reason": "missing_unique_field", "record": record})
                continue

            key = tuple(record.get(f) for f in unique_fields)
            existing = existing_by_key.get(key)

            if existing is None:
                would_create.append({"index": idx, "record": record})
            else:
                diff = _compute_diff(existing, record)
                if diff:
                    would_update.append({"index": idx, "pk": existing.pk, "diff": diff})
                else:
                    would_skip.append({"index": idx, "reason": "identical", "pk": existing.pk})

        transaction.savepoint_rollback(sid)

    return {
        "module": module,
        "file_format": file_format,
        "total_records": len(records),
        "valid_count": valid_count,
        "would_create": would_create,
        "would_update": would_update,
        "would_skip": would_skip,
        "validation_errors": validation_errors,
        "summary": {
            "create": len(would_create),
            "update": len(would_update),
            "skip": len(would_skip),
            "errors": len(validation_errors),
        },
    }
