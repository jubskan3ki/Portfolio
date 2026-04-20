"""Service d'import de donnees utilisant le Strategy Pattern."""

import csv
import io
import json
import logging
from typing import Any

import openpyxl
from django.apps import apps
from django.core.files.uploadedfile import UploadedFile
from django.db import DatabaseError, IntegrityError, OperationalError, models, transaction
from django.utils import timezone

from ..models import ImportJob
from .strategies import CsvImportStrategy, ImportStrategy, JsonImportStrategy, XlsxImportStrategy
from .validators import DataValidator

logger = logging.getLogger("core.transfer")


class ImporterService:
    """Service pour l'import de donnees utilisant le Strategy Pattern."""

    _strategies: list[ImportStrategy] = [
        JsonImportStrategy(),
        CsvImportStrategy(),
        XlsxImportStrategy(),
    ]

    SUPPORTED_MODULES = ["articles", "projects", "stacks", "experiences"]

    # Structure: module -> field_name -> (app_label, model_name, lookup_field)
    FK_MAPPINGS: dict[str, dict[str, tuple[str, str, str]]] = {
        "articles": {
            "category": ("articles", "Category", "name"),
        },
        "projects": {
            "category": ("projects", "ProjectCategory", "name"),
            "status": ("projects", "ProjectStatus", "name"),
        },
        "stacks": {
            "category": ("stacks", "StackCategory", "name"),
        },
        "experiences": {
            "type": ("experiences", "ExperienceType", "name"),
        },
    }

    M2M_MAPPINGS: dict[str, dict[str, tuple[str, str, str]]] = {
        "articles": {
            "tags": ("articles", "Tag", "name"),
        },
        "projects": {},
        "stacks": {},
        "experiences": {},
    }

    # str pour champ unique, tuple pour cle composee (update_or_create)
    UNIQUE_FIELDS: dict[str, str | tuple[str, ...]] = {
        "articles": "slug",
        "projects": "slug",
        "stacks": "slug",
        "experiences": ("title", "company"),  # Cle composee pour eviter les doublons
    }

    @classmethod
    def _get_strategy(cls, filename: str) -> ImportStrategy:
        """Get the appropriate strategy for the given filename."""
        for strategy in cls._strategies:
            if strategy.can_handle(filename):
                return strategy
        extensions = [ext for s in cls._strategies for ext in s.file_extensions]
        raise ValueError(f"Format non supporte. Extensions valides: {extensions}")

    @classmethod
    def detect_format(cls, filename: str) -> str:
        """Detecte le format du fichier."""
        strategy = cls._get_strategy(filename)
        return strategy.format_name

    @classmethod
    def validate_module(cls, module: str) -> None:
        """Valide que le module est supporte."""
        if module not in cls.SUPPORTED_MODULES:
            raise ValueError(f"Module '{module}' non supporte. Modules valides: {cls.SUPPORTED_MODULES}")

    @classmethod
    def parse_file(cls, file: UploadedFile) -> tuple[list[dict[str, Any]], str]:
        """Parse le fichier uploade via la strategie appropriee; retourne (records, format)."""
        file.seek(0)
        filename = file.name or "unknown"
        strategy = cls._get_strategy(filename)
        records = strategy.parse(file)
        return records, strategy.format_name

    @classmethod
    def _parse_json(cls, file: UploadedFile) -> list[dict[str, Any]]:
        content = file.read().decode("utf-8")
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Fichier JSON invalide: {e}") from e

        # Accepte liste plate ou enveloppe {"data": [...]}
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "data" in data:
            return data["data"]

        raise ValueError("Format JSON invalide. Attendu: liste ou {'data': [...]}")

    @classmethod
    def _parse_csv(cls, file: UploadedFile) -> list[dict[str, Any]]:
        content = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        records = []

        for row in reader:
            cleaned_row = {}
            for key, value in row.items():
                if key is None:
                    continue
                if value and isinstance(value, str) and value.startswith(("[", "{")):
                    try:
                        cleaned_row[key] = json.loads(value)
                    except json.JSONDecodeError:
                        cleaned_row[key] = value
                else:
                    cleaned_row[key] = value
            records.append(cleaned_row)

        return records

    @classmethod
    def _parse_xlsx(cls, file: UploadedFile) -> list[dict[str, Any]]:
        workbook = openpyxl.load_workbook(file, read_only=True, data_only=True)
        sheet = workbook.active
        records: list[dict[str, Any]] = []

        if sheet is None:
            workbook.close()
            return records

        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return records

        headers = []
        for i, h in enumerate(rows[0]):
            if h is not None:
                headers.append(str(h).strip())
            else:
                headers.append(f"col_{i}")

        for row in rows[1:]:
            record = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    header = headers[i]
                    if isinstance(value, str) and value.startswith(("[", "{")):
                        try:
                            record[header] = json.loads(value)
                        except json.JSONDecodeError:
                            record[header] = value
                    else:
                        record[header] = value
            if any(v is not None and v != "" for v in record.values()):
                records.append(record)

        workbook.close()
        return records

    @classmethod
    def preview_import(
        cls,
        file: UploadedFile,
        module: str,
        limit: int = 5,
    ) -> dict[str, Any]:
        """Preview les donnees avant import: preview_data, columns, total_records, validation_errors."""
        cls.validate_module(module)

        records, file_format = cls.parse_file(file)
        file.seek(0)

        preview_valid_count, errors = DataValidator.validate_batch(module, records[:limit])

        columns = list(records[0].keys()) if records else []

        return {
            "total_records": len(records),
            "preview_data": records[:limit],
            "columns": columns,
            "validation_errors": errors,
            "file_format": file_format,
            "valid_count": preview_valid_count,
        }

    @classmethod
    def create_import_job(
        cls,
        user: Any,
        module: str,
        file: UploadedFile,
    ) -> ImportJob:
        """Cree un job d'import."""
        cls.validate_module(module)
        filename = file.name or "unknown"
        file_format = cls.detect_format(filename)

        return ImportJob.objects.create(
            user=user,
            module=module,
            status=ImportJob.Status.PENDING,
            original_filename=file.name,
            file_format=file_format,
        )

    IMAGE_FIELDS: dict[str, str] = {
        "articles": "image",
        "projects": "image",
        "stacks": "logo",
        "experiences": "logo",
    }

    @classmethod
    def execute_import(
        cls,
        job: ImportJob,
        file: UploadedFile,
        *,
        update_existing: bool = False,
        images: dict[str, UploadedFile] | None = None,
    ) -> ImportJob:
        """Execute l'import de donnees."""
        job.status = ImportJob.Status.VALIDATING
        job.save(update_fields=["status"])

        try:
            file.seek(0)

            records, _ = cls.parse_file(file)
            job.total_records = len(records)
            job.save(update_fields=["total_records"])

            if not records:
                job.status = ImportJob.Status.COMPLETED
                job.completed_at = timezone.now()
                job.save()
                return job

            _, validation_errors = DataValidator.validate_batch(job.module, records)

            if validation_errors:
                job.errors = validation_errors
                job.error_count = len(validation_errors)
                job.save(update_fields=["errors", "error_count"])

            job.status = ImportJob.Status.PROCESSING
            job.save(update_fields=["status"])

            model_class = DataValidator.get_model_class(job.module)
            if not model_class:
                raise ValueError(f"Modele non trouve pour le module '{job.module}'")

            import_errors: list[dict[str, Any]] = []
            success_count = 0
            processed_count = 0

            image_field = cls.IMAGE_FIELDS.get(job.module)

            for i, record in enumerate(records, start=1):
                try:
                    # Savepoint par enregistrement pour isoler les rollbacks
                    with transaction.atomic():
                        cleaned_data = DataValidator.clean_data(record, job.module)
                        cls._import_record(
                            model_class,
                            cleaned_data,
                            job.module,
                            update_existing=update_existing,
                            images=images,
                            image_field=image_field,
                        )
                        success_count += 1
                except (IntegrityError, ValueError, TypeError, KeyError, AttributeError) as e:
                    logger.warning("Erreur import ligne %d: %s", i, str(e))
                    import_errors.append({"row": i, "field": "general", "message": str(e)})

                processed_count += 1

            job.success_count = success_count
            job.processed_records = processed_count
            if import_errors:
                existing_errors = job.errors if isinstance(job.errors, list) else []
                job.errors = existing_errors + import_errors
                job.error_count = len(job.errors)

            if job.error_count == 0:
                job.status = ImportJob.Status.COMPLETED
            elif job.success_count > 0:
                job.status = ImportJob.Status.PARTIALLY_COMPLETED
            else:
                job.status = ImportJob.Status.FAILED

            job.completed_at = timezone.now()
            job.save()

        except (DatabaseError, OperationalError, ValueError, ImportError) as e:
            logger.exception("Erreur lors de l'import du module %s", job.module)
            job.status = ImportJob.Status.FAILED
            if not job.errors:
                job.errors = []
            job.errors.append({"row": 0, "field": "system", "message": str(e)})
            job.save()

        return job

    @classmethod
    def _import_record(
        cls,
        model_class: type[models.Model],
        data: dict[str, Any],
        module: str,
        *,
        update_existing: bool,
        images: dict[str, UploadedFile] | None = None,
        image_field: str | None = None,
    ) -> Any:
        if image_field and image_field in data:
            image_key = data.get(image_field)
            if isinstance(image_key, str) and images and image_key in images:
                data[image_field] = images[image_key]
            elif isinstance(image_key, str):
                # Evite SuspiciousFileOperation si le chemin est absolu (/media/...)
                data.pop(image_field, None)

        # get_fields() inclut les reverse relations non assignables; on les exclut via auto_created.
        model_field_names = {
            f.name
            for f in model_class._meta.get_fields()
            if not getattr(f, "auto_created", False) or getattr(f, "concrete", False)
        }
        data = {k: v for k, v in data.items() if k in model_field_names}

        data = cls._resolve_foreign_keys(data, module)

        m2m_fields = cls._extract_m2m_fields(data, model_class)
        m2m_fields = cls._resolve_m2m_fields(m2m_fields, module)

        unique_fields = cls.UNIQUE_FIELDS.get(module, "id")

        if isinstance(unique_fields, tuple):
            unique_lookup = {}
            all_values_present = True
            for field in unique_fields:
                value = data.get(field)
                if value is None:
                    all_values_present = False
                    break
                unique_lookup[field] = value

            manager = model_class._default_manager

            if update_existing and all_values_present:
                defaults = {k: v for k, v in data.items() if k not in unique_fields}
                # select_related(None) pour eviter FOR UPDATE sur outer joins nullable
                qs = manager.all().select_related(None)
                instance, _ = qs.update_or_create(
                    **unique_lookup,
                    defaults=defaults,
                )
            else:
                instance = manager.create(**data)
        else:
            unique_value = data.get(unique_fields)
            manager = model_class._default_manager

            if update_existing and unique_value:
                defaults = {k: v for k, v in data.items() if k != unique_fields}
                # select_related(None) pour eviter FOR UPDATE sur outer joins nullable
                qs = manager.all().select_related(None)
                instance, _ = qs.update_or_create(
                    **{unique_fields: unique_value},
                    defaults=defaults,
                )
            else:
                instance = manager.create(**data)

        for field_name, values in m2m_fields.items():
            if hasattr(instance, field_name) and values:
                m2m_manager = getattr(instance, field_name)
                if isinstance(values, list):
                    m2m_manager.set(values)

        return instance

    @classmethod
    def _resolve_foreign_keys(cls, data: dict[str, Any], module: str) -> dict[str, Any]:
        """Resout les cles etrangeres."""
        mappings = cls.FK_MAPPINGS.get(module, {})
        resolved = dict(data)

        for field, (app_label, model_name, lookup_field) in mappings.items():
            if field in resolved and resolved[field] is not None:
                value = resolved[field]
                # Si c'est deja un objet, ne pas le resoudre
                if not isinstance(value, str | int):
                    continue

                try:
                    model = apps.get_model(app_label, model_name)
                except LookupError:
                    logger.warning("Modele %s.%s non trouve", app_label, model_name)
                    continue

                try:
                    obj = model.objects.get(**{lookup_field: value})
                    resolved[field] = obj
                except model.DoesNotExist:
                    # Create if it doesn't exist
                    logger.info("Creation de %s avec %s=%s", model_name, lookup_field, value)
                    # Build creation data - include name if model has it
                    create_data = {lookup_field: value}
                    if hasattr(model, "name") and lookup_field != "name":
                        create_data["name"] = value
                    obj = model.objects.create(**create_data)
                    resolved[field] = obj

        return resolved

    @classmethod
    def _extract_m2m_fields(cls, data: dict[str, Any], model_class: type[models.Model]) -> dict[str, list]:
        """Extrait et supprime les champs M2M de data."""
        m2m_fields = {}
        m2m_field_names = [f.name for f in model_class._meta.get_fields() if f.many_to_many and not f.auto_created]

        for field_name in m2m_field_names:
            if field_name in data:
                value = data.pop(field_name)
                if value is not None:
                    m2m_fields[field_name] = value

        return m2m_fields

    @classmethod
    def _resolve_m2m_fields(cls, m2m_fields: dict[str, list | Any], module: str) -> dict[str, list | Any]:
        """Resout les valeurs M2M en objets de base de donnees."""
        mappings = cls.M2M_MAPPINGS.get(module, {})
        resolved: dict[str, list | Any] = {}

        for field_name, values in m2m_fields.items():
            if not isinstance(values, list):
                resolved[field_name] = values
                continue

            # Si pas de mapping, garder les valeurs telles quelles (supposees etre des PKs)
            if field_name not in mappings:
                resolved[field_name] = values
                continue

            app_label, model_name, lookup_field = mappings[field_name]
            try:
                model = apps.get_model(app_label, model_name)
            except LookupError:
                logger.warning("Modele M2M %s.%s non trouve", app_label, model_name)
                resolved[field_name] = values
                continue

            resolved_values = []
            for value in values:
                # Si c'est deja un int (PK), l'utiliser directement
                if isinstance(value, int):
                    resolved_values.append(value)
                    continue

                # Sinon, chercher ou creer l'objet par le lookup_field
                try:
                    obj = model.objects.get(**{lookup_field: value})
                    resolved_values.append(obj.pk)
                except model.DoesNotExist:
                    # Creer l'objet s'il n'existe pas
                    logger.info("Creation de %s avec %s=%s", model_name, lookup_field, value)
                    obj = model.objects.create(**{lookup_field: value})
                    resolved_values.append(obj.pk)

            resolved[field_name] = resolved_values

        return resolved
