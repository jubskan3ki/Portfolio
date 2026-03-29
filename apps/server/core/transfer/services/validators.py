"""Validateurs pour l'import de donnees."""

import logging
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from django.apps import apps
from django.db import models

from ..registry import MODULE_REGISTRY

logger = logging.getLogger("core.transfer")

# Formats de date supportes pour l'import
DATE_FORMATS = [
    "%Y-%m-%d",  # 2024-01-15
    "%d/%m/%Y",  # 15/01/2024
    "%d-%m-%Y",  # 15-01-2024
    "%Y/%m/%d",  # 2024/01/15
    "%m/%d/%Y",  # 01/15/2024 (US format)
    "%d %b %Y",  # 15 Jan 2024
    "%d %B %Y",  # 15 January 2024
    "%Y-%m-%dT%H:%M:%S",  # ISO format with time
    "%Y-%m-%dT%H:%M:%SZ",  # ISO format with Z
    "%Y-%m-%dT%H:%M:%S.%f",  # ISO format with microseconds
    "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO format with microseconds and Z
]


def parse_date(value: Any) -> date | None:
    """Parse une valeur en date."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if not isinstance(value, str):
        return None

    value = value.strip()
    if not value:
        return None

    # Essayer chaque format
    for fmt in DATE_FORMATS:
        try:
            parsed = datetime.strptime(value, fmt).replace(tzinfo=UTC)
            return parsed.date()
        except ValueError:
            continue

    logger.warning("Impossible de parser la date: %s", value)
    return None


class DataValidator:
    """Validateur de donnees pour l'import."""

    # Champs requis par module (issus du registre centralise)

    # Champs a ignorer lors de l'import (auto-generes, systeme)
    IGNORED_FIELDS: list[str] = [
        "id",
        "pk",
        "created_at",
        "updated_at",
        "created_date",
        "updated_date",
        "view_count",
        "reference_id",
        "ip_address",
        "views",  # view_count renomme
        "is_current",  # is_current est une propriete calculee
        "period",  # champ calcule automatiquement
        "cover_image",  # alias de image
        "skills",  # n'existe pas dans le modele Experience
    ]

    # Champs ignores par module specifique
    MODULE_IGNORED_FIELDS: dict[str, list[str]] = {
        "stacks": ["experience"],  # experience (mois) n'existe pas dans le modele
    }

    # Types de champs pour conversion
    FIELD_TYPES: dict[str, dict[str, str]] = {
        "stacks": {
            "level": "decimal",
            "started_date": "date",
        },
        "articles": {
            "read_time": "integer",
            "is_published": "boolean",
            "is_featured": "boolean",
            "published_date": "date",
        },
        "experiences": {
            "start_date": "date",
            "end_date": "date",
            "is_current": "boolean",
        },
        "projects": {
            "is_featured": "boolean",
            "date": "date",
        },
    }

    # Mapping des champs camelCase vers snake_case
    FIELD_NAME_MAPPING: dict[str, str] = {
        "startDate": "start_date",
        "endDate": "end_date",
        "readTime": "read_time",
        "isPublished": "is_published",
        "isFeatured": "is_featured",
        "publishedDate": "published_date",
        "viewCount": "view_count",
        "createdAt": "created_at",
        "updatedAt": "updated_at",
        "websiteLabel": "website_label",
        "githubLabel": "github_label",
        "firstRelease": "first_release",
        "longDescription": "long_description",
    }

    # Mapping de champs specifique par module (applique apres le mapping global)
    MODULE_FIELD_NAME_MAPPING: dict[str, dict[str, str]] = {
        "articles": {"date": "published_date"},
    }

    @classmethod
    def get_model_class(cls, module: str) -> type[models.Model] | None:
        """Recupere la classe du modele pour un module."""
        config = MODULE_REGISTRY.get(module)
        if not config:
            logger.warning("Module '%s' non supporte", module)
            return None

        try:
            return apps.get_model(config["app_label"], config["model_name"])
        except LookupError:
            logger.exception("Modele non trouve pour %s", module)
            return None

    @classmethod
    def validate_record(
        cls,
        module: str,
        data: dict[str, Any],
        row_number: int,
    ) -> tuple[bool, list[dict[str, Any]]]:
        """Valide un enregistrement pour l'import.

        Returns:
            Tuple (is_valid, errors)
        """
        # Convertir les noms de champs camelCase en snake_case pour la validation
        module_mapping = cls.MODULE_FIELD_NAME_MAPPING.get(module, {})
        normalized_data = {module_mapping.get(k, cls.FIELD_NAME_MAPPING.get(k, k)): v for k, v in data.items()}

        # Verification des champs requis
        config = MODULE_REGISTRY.get(module, {})
        required = config.get("required_fields", [])
        errors: list[dict[str, Any]] = [
            {
                "row": row_number,
                "field": field,
                "message": f"Le champ '{field}' est requis",
            }
            for field in required
            if field not in normalized_data or normalized_data[field] is None or normalized_data[field] == ""
        ]

        # Validation des types de champs
        field_types = cls.FIELD_TYPES.get(module, {})
        for field, field_type in field_types.items():
            if field in normalized_data and normalized_data[field] is not None:
                value = normalized_data[field]
                if field_type == "integer" and not isinstance(value, int):
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        errors.append(
                            {
                                "row": row_number,
                                "field": field,
                                "message": f"Le champ '{field}' doit etre un entier",
                            }
                        )
                elif field_type == "decimal" and not isinstance(value, int | float | Decimal):
                    try:
                        Decimal(str(value))
                    except (ValueError, InvalidOperation):
                        errors.append(
                            {
                                "row": row_number,
                                "field": field,
                                "message": f"Le champ '{field}' doit etre un nombre decimal",
                            }
                        )

        return len(errors) == 0, errors

    @classmethod
    def clean_data(cls, data: dict[str, Any], module: str | None = None) -> dict[str, Any]:
        """Nettoie les donnees avant import."""
        # Pre-traitement : isCurrent=true => end_date=null
        if module == "experiences":
            is_current = data.get("isCurrent", data.get("is_current"))
            if isinstance(is_current, bool) and is_current:
                data["endDate"] = None
                data["end_date"] = None

        cleaned = {}
        field_types = cls.FIELD_TYPES.get(module, {}) if module else {}
        module_ignored = cls.MODULE_IGNORED_FIELDS.get(module, []) if module else []

        for key, value in data.items():
            # Ignorer les champs systeme globaux
            if key in cls.IGNORED_FIELDS:
                continue

            # Ignorer les champs specifiques au module
            if key in module_ignored:
                continue

            # Convertir les noms de champs camelCase en snake_case
            module_mapping = cls.MODULE_FIELD_NAME_MAPPING.get(module, {}) if module else {}
            field_name = module_mapping.get(key, cls.FIELD_NAME_MAPPING.get(key, key))

            # Si le champ converti est dans IGNORED_FIELDS, l'ignorer
            if field_name in cls.IGNORED_FIELDS or field_name in module_ignored:
                continue

            cleaned_value = value

            # Convertir les valeurs vides en None
            if value == "" or value == "null" or value == "NULL":
                cleaned_value = None
            # Convertir selon le type de champ
            elif field_name in field_types:
                field_type = field_types[field_name]
                if field_type == "date":
                    cleaned_value = parse_date(value)
                elif field_type == "integer":
                    try:
                        cleaned_value = int(value) if value is not None else None
                    except (ValueError, TypeError):
                        cleaned_value = value
                elif field_type == "decimal":
                    try:
                        cleaned_value = Decimal(str(value)) if value is not None else None
                    except (ValueError, InvalidOperation):
                        cleaned_value = value
                elif field_type == "boolean":
                    if isinstance(value, str):
                        lower_value = value.lower()
                        cleaned_value = lower_value in ("true", "yes", "1", "oui")
                    else:
                        cleaned_value = bool(value)
            # Convertir les booleens par defaut (si pas dans field_types)
            elif isinstance(value, str):
                lower_value = value.lower()
                if lower_value in ("true", "yes", "1", "oui"):
                    cleaned_value = True
                elif lower_value in ("false", "no", "0", "non"):
                    cleaned_value = False

            cleaned[field_name] = cleaned_value

        return cleaned

    @classmethod
    def validate_batch(
        cls,
        module: str,
        records: list[dict[str, Any]],
    ) -> tuple[int, list[dict[str, Any]]]:
        """Valide un lot d'enregistrements.

        Returns:
            Tuple (valid_count, all_errors)
        """
        all_errors: list[dict[str, Any]] = []
        valid_count = 0

        for i, record in enumerate(records, start=1):
            is_valid, errors = cls.validate_record(module, record, i)
            if is_valid:
                valid_count += 1
            else:
                all_errors.extend(errors)

        return valid_count, all_errors
