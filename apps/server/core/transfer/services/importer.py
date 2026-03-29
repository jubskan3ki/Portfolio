"""Service d'import de donnees utilisant le Strategy Pattern."""

import csv
import io
import json
import logging
from typing import TYPE_CHECKING, Any

import openpyxl
from django.apps import apps
from django.core.files.uploadedfile import UploadedFile
from django.db import DatabaseError, IntegrityError, OperationalError, transaction
from django.utils import timezone

if TYPE_CHECKING:
    from django.db import models

from ..models import ImportJob
from .strategies import CsvImportStrategy, ImportStrategy, JsonImportStrategy, XlsxImportStrategy
from .validators import DataValidator

logger = logging.getLogger("core.transfer")


class ImporterService:
    """Service pour l'import de donnees utilisant le Strategy Pattern."""

    # Registry des strategies d'import
    _strategies: list[ImportStrategy] = [
        JsonImportStrategy(),
        CsvImportStrategy(),
        XlsxImportStrategy(),
    ]

    # Modules supportes
    SUPPORTED_MODULES = ["articles", "projects", "stacks", "experiences"]

    # Mapping des FK (field_name -> (app_label, model_name, lookup_field))
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

    # Mapping des M2M (field_name -> (app_label, model_name, lookup_field))
    M2M_MAPPINGS: dict[str, dict[str, tuple[str, str, str]]] = {
        "articles": {
            "tags": ("articles", "Tag", "name"),
        },
        "projects": {},
        "stacks": {},
        "experiences": {},
    }

    # Champ unique par module pour update_or_create
    # Peut etre un str pour un champ unique ou un tuple pour une cle composee
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
        """Parse le fichier uploade via la strategie appropriee.

        Returns:
            Tuple (records, format)
        """
        # Reset file position in case it was read before
        file.seek(0)

        filename = file.name or "unknown"
        strategy = cls._get_strategy(filename)
        records = strategy.parse(file)
        return records, strategy.format_name

    @classmethod
    def _parse_json(cls, file: UploadedFile) -> list[dict[str, Any]]:
        """Parse un fichier JSON."""
        content = file.read().decode("utf-8")
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Fichier JSON invalide: {e}") from e

        # Handle both flat list and wrapped format
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "data" in data:
            return data["data"]

        raise ValueError("Format JSON invalide. Attendu: liste ou {'data': [...]}")

    @classmethod
    def _parse_csv(cls, file: UploadedFile) -> list[dict[str, Any]]:
        """Parse un fichier CSV."""
        content = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        records = []

        for row in reader:
            # Try to parse JSON strings back to objects
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
        """Parse un fichier Excel."""
        workbook = openpyxl.load_workbook(file, read_only=True, data_only=True)
        sheet = workbook.active
        records: list[dict[str, Any]] = []

        if sheet is None:
            workbook.close()
            return records

        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return records

        # Build headers from first row
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
                    # Try to parse JSON strings
                    if isinstance(value, str) and value.startswith(("[", "{")):
                        try:
                            record[header] = json.loads(value)
                        except json.JSONDecodeError:
                            record[header] = value
                    else:
                        record[header] = value
            # Only add non-empty records
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
        """Preview les donnees avant import.

        Returns:
            Dict avec preview_data, columns, total_records, validation_errors
        """
        cls.validate_module(module)

        records, file_format = cls.parse_file(file)

        # Reset file position for later use
        file.seek(0)

        # Validate first records
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

    # Image field names per module
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
            # Reset file position
            file.seek(0)

            records, _ = cls.parse_file(file)
            job.total_records = len(records)
            job.save(update_fields=["total_records"])

            if not records:
                job.status = ImportJob.Status.COMPLETED
                job.completed_at = timezone.now()
                job.save()
                return job

            # Validate all records
            _, validation_errors = DataValidator.validate_batch(job.module, records)

            if validation_errors:
                job.errors = validation_errors
                job.error_count = len(validation_errors)
                job.save(update_fields=["errors", "error_count"])

            job.status = ImportJob.Status.PROCESSING
            job.save(update_fields=["status"])

            # Import records
            model_class = DataValidator.get_model_class(job.module)
            if not model_class:
                raise ValueError(f"Modele non trouve pour le module '{job.module}'")

            # Accumuler les erreurs et les succes en memoire
            # Utiliser des savepoints pour permettre le rollback par enregistrement
            import_errors: list[dict[str, Any]] = []
            success_count = 0
            processed_count = 0

            # Get image field for this module
            image_field = cls.IMAGE_FIELDS.get(job.module)

            for i, record in enumerate(records, start=1):
                try:
                    # Utiliser un savepoint pour chaque enregistrement
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

            # Mettre a jour le job apres tous les imports
            job.success_count = success_count
            job.processed_records = processed_count
            if import_errors:
                existing_errors = job.errors if isinstance(job.errors, list) else []
                job.errors = existing_errors + import_errors
                job.error_count = len(job.errors)

            # Determine final status
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
        model_class: "type[models.Model]",
        data: dict[str, Any],
        module: str,
        *,
        update_existing: bool,
        images: dict[str, UploadedFile] | None = None,
        image_field: str | None = None,
    ) -> Any:
        """Importe un enregistrement."""
        # Handle image field - match key in data with uploaded image
        if image_field and image_field in data:
            image_key = data.get(image_field)
            if isinstance(image_key, str) and images and image_key in images:
                data[image_field] = images[image_key]
            elif isinstance(image_key, str):
                # Remove string path if no matching uploaded image — prevents
                # SuspiciousFileOperation when the path is absolute (e.g. /media/...)
                data.pop(image_field, None)

        # Filter out fields that don't exist as concrete/forward fields on the model.
        # get_fields() includes reverse relations (e.g. resources on Stack) which
        # cannot be directly assigned — exclude them via the auto_created check.
        model_field_names = {
            f.name
            for f in model_class._meta.get_fields()
            if not getattr(f, "auto_created", False) or getattr(f, "concrete", False)
        }
        data = {k: v for k, v in data.items() if k in model_field_names}

        # Handle foreign keys
        data = cls._resolve_foreign_keys(data, module)

        # Handle M2M fields (remove from data, process after save)
        m2m_fields = cls._extract_m2m_fields(data, model_class)

        # Resolve M2M field values (names -> PKs)
        m2m_fields = cls._resolve_m2m_fields(m2m_fields, module)

        # Get unique identifier(s)
        unique_fields = cls.UNIQUE_FIELDS.get(module, "id")

        # Handle compound unique keys (tuple) or single field (str)
        if isinstance(unique_fields, tuple):
            # Cle composee: verifier que toutes les valeurs sont presentes
            unique_lookup = {}
            all_values_present = True
            for field in unique_fields:
                value = data.get(field)
                if value is None:
                    all_values_present = False
                    break
                unique_lookup[field] = value

            if update_existing and all_values_present:
                # Remove unique fields from defaults
                defaults = {k: v for k, v in data.items() if k not in unique_fields}
                # Clear select_related to avoid FOR UPDATE on nullable outer joins
                qs = model_class.objects.all().select_related(None)
                instance, _ = qs.update_or_create(
                    **unique_lookup,
                    defaults=defaults,
                )
            else:
                instance = model_class.objects.create(**data)
        else:
            # Champ unique simple
            unique_value = data.get(unique_fields)

            if update_existing and unique_value:
                # Remove unique field from defaults to avoid constraint issues
                defaults = {k: v for k, v in data.items() if k != unique_fields}
                # Clear select_related to avoid FOR UPDATE on nullable outer joins
                qs = model_class.objects.all().select_related(None)
                instance, _ = qs.update_or_create(
                    **{unique_fields: unique_value},
                    defaults=defaults,
                )
            else:
                instance = model_class.objects.create(**data)

        # Handle M2M fields
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
    def _extract_m2m_fields(cls, data: dict[str, Any], model_class: "type[models.Model]") -> dict[str, list]:
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
