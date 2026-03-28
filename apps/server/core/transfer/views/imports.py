"""Views pour l'import de donnees."""

import logging
from pathlib import Path
from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.db import DatabaseError, OperationalError
from django.utils.datastructures import MultiValueDict

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from utils.upload import extract_images_from_files

from ..models import ImportJob
from ..serializers import ImportJobSerializer
from ..serializers.imports import ImportPreviewSerializer
from ..services import ImporterService
from ..throttles import ImportThrottle

logger = logging.getLogger("core.transfer")

ALLOWED_IMPORT_EXTENSIONS = {".json", ".csv", ".xlsx"}
ALLOWED_IMPORT_MIME_TYPES = {
    "application/json",
    "text/csv",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}
MAX_IMPORT_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_import_file(file: UploadedFile) -> str | None:
    """Valide le type et la taille du fichier d'import. Retourne un message d'erreur ou None."""
    ext = Path(file.name or "").suffix.lower()
    if ext not in ALLOWED_IMPORT_EXTENSIONS:
        allowed = ", ".join(ALLOWED_IMPORT_EXTENSIONS)
        return f"Extension '{ext}' non autorisee. Acceptees: {allowed}"

    content_type = getattr(file, "content_type", None)
    if content_type and content_type not in ALLOWED_IMPORT_MIME_TYPES:
        return f"Type MIME '{content_type}' non autorise."

    if file.size and file.size > MAX_IMPORT_FILE_SIZE:
        max_mb = MAX_IMPORT_FILE_SIZE // (1024 * 1024)
        return f"Fichier trop volumineux. Maximum: {max_mb} Mo."

    return None


class ImportViewSet(viewsets.ViewSet):
    """ViewSet pour l'import de donnees."""

    permission_classes = [IsAdminUser]
    throttle_classes = [ImportThrottle]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        description="Preview des donnees avant import",
        parameters=[
            OpenApiParameter(
                "module",
                location=OpenApiParameter.PATH,
                description="Module cible",
                type=str,
                required=True,
            ),
            OpenApiParameter(
                "file",
                location=OpenApiParameter.QUERY,
                description="Fichier a importer (multipart/form-data)",
                type=str,
                required=True,
            ),
        ],
        responses={
            200: ImportPreviewSerializer,
            400: OpenApiResponse(description="Requete invalide"),
        },
    )
    def preview(self, request: Request, module: str) -> Response:
        """Preview des donnees avant import."""
        files = cast(MultiValueDict, request.FILES)
        file = files.get("file")
        if not file:
            return Response(
                {"error": "Fichier requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validation_error = validate_import_file(file)
        if validation_error:
            return Response(
                {"error": validation_error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            preview_data = ImporterService.preview_import(
                file=file,
                module=module,
                limit=10,
            )

            return Response(
                ImportPreviewSerializer(preview_data).data,
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (DatabaseError, OperationalError, ImportError):
            logger.exception("Erreur lors du preview")
            return Response(
                {"error": "Erreur lors de la lecture du fichier"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        description="Importe les donnees dans un module",
        parameters=[
            OpenApiParameter(
                "module",
                location=OpenApiParameter.PATH,
                description="Module cible",
                type=str,
                required=True,
            ),
            OpenApiParameter(
                "update_existing",
                location=OpenApiParameter.QUERY,
                description="Mettre a jour les enregistrements existants",
                type=bool,
                default=False,
            ),
        ],
        responses={
            201: ImportJobSerializer,
            400: OpenApiResponse(description="Requete invalide"),
        },
    )
    def import_module(self, request: Request, module: str) -> Response:
        """Importe les donnees dans un module specifique."""
        files = cast(MultiValueDict, request.FILES)
        file = files.get("file")
        if not file:
            return Response(
                {"error": "Fichier requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validation_error = validate_import_file(file)
        if validation_error:
            return Response(
                {"error": validation_error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = cast(MultiValueDict, request.data)
        update_existing = data.get("update_existing", False)
        if isinstance(update_existing, str):
            update_existing = update_existing.lower() in ("true", "1", "yes")

        images = extract_images_from_files(files)

        try:
            # Create job
            job = ImporterService.create_import_job(
                user=request.user,
                module=module,
                file=file,
            )

            # Execute import
            job = ImporterService.execute_import(
                job=job,
                file=file,
                update_existing=update_existing,
                images=images,
            )

            status_code = (
                status.HTTP_201_CREATED
                if job.status in [ImportJob.Status.COMPLETED, ImportJob.Status.PARTIALLY_COMPLETED]
                else status.HTTP_400_BAD_REQUEST
            )

            return Response(
                ImportJobSerializer(job).data,
                status=status_code,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (DatabaseError, OperationalError):
            logger.exception("Erreur lors de l'import")
            return Response(
                {"error": "Erreur lors de l'import"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        description="Import bulk depuis plusieurs fichiers",
        responses={201: OpenApiResponse(description="Liste des jobs d'import")},
    )
    def bulk_import(self, request: Request) -> Response:
        """Import bulk de plusieurs fichiers."""
        request_files = cast(MultiValueDict, request.FILES)
        files = request_files.getlist("files")
        request_data = cast(MultiValueDict, request.data)
        modules = request_data.getlist("modules")

        if len(files) != len(modules):
            return Response(
                {"error": "Le nombre de fichiers doit correspondre au nombre de modules"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        jobs: list[dict[str, Any]] = []
        for file, module in zip(files, modules, strict=True):
            try:
                job = ImporterService.create_import_job(
                    user=request.user,
                    module=module,
                    file=file,
                )
                job = ImporterService.execute_import(job=job, file=file)
                jobs.append(ImportJobSerializer(job).data)
            except (ValueError, DatabaseError, OperationalError) as e:
                jobs.append(
                    {
                        "module": module,
                        "filename": file.name,
                        "error": str(e),
                    }
                )

        return Response({"imports": jobs}, status=status.HTTP_201_CREATED)
