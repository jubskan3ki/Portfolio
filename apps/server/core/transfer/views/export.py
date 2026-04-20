"""Views pour l'export de donnees."""

import logging

from django.db import DatabaseError, OperationalError
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import ExportJob
from ..serializers import ExportJobSerializer, ExportRequestSerializer
from ..services import ExporterService
from ..throttles import ExportThrottle

logger = logging.getLogger("core.transfer")


class ExportModuleView(APIView):
    """Vue pour l'export d'un module specifique."""

    permission_classes = [IsAdminUser]
    throttle_classes = [ExportThrottle]

    @extend_schema(
        description="Exporte les donnees d'un module",
        parameters=[
            OpenApiParameter(
                "module",
                location=OpenApiParameter.PATH,
                description="Module a exporter (articles, projects, stacks, experiences, contacts)",
                type=str,
                required=True,
            ),
            OpenApiParameter(
                "export_format",
                location=OpenApiParameter.QUERY,
                description="Format d'export (json, csv, xlsx)",
                type=str,
                default="json",
            ),
        ],
        responses={
            200: ExportJobSerializer,
            400: OpenApiResponse(description="Requete invalide"),
            403: OpenApiResponse(description="Non autorise"),
        },
    )
    def get(self, request: Request, module: str) -> Response:
        """Exporte les donnees d'un module specifique."""
        export_format = request.query_params.get("export_format", "json")

        serializer = ExportRequestSerializer(
            data={
                "module": module,
                "format": export_format,
                "filters": {
                    k: v
                    for k, v in request.query_params.items()
                    if k not in ("export_format", "format", "page", "page_size")
                },
            }
        )

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            filters = getattr(serializer.validated_data, "get", lambda _: None)("filters")
            job = ExporterService.create_export_job(
                user=request.user,
                module=module,
                export_format=export_format,
                filters=filters,
            )

            if job.status == ExportJob.Status.FAILED:
                return Response(
                    {"error": job.error_message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                ExportJobSerializer(job, context={"request": request}).data,
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (DatabaseError, OperationalError):
            logger.exception("Erreur lors de l'export")
            return Response(
                {"error": "Erreur lors de l'export"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExportDownloadView(APIView):
    """Vue pour telecharger directement un export."""

    permission_classes = [IsAdminUser]
    throttle_classes = [ExportThrottle]

    @extend_schema(
        description="Telecharge directement le fichier d'export",
        parameters=[
            OpenApiParameter(
                "module",
                location=OpenApiParameter.PATH,
                description="Module a exporter",
                type=str,
                required=True,
            ),
            OpenApiParameter(
                "export_format",
                location=OpenApiParameter.QUERY,
                description="Format d'export (json, csv, xlsx)",
                type=str,
                default="json",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Fichier d'export"),
            400: OpenApiResponse(description="Requete invalide"),
            401: OpenApiResponse(description="Non authentifie"),
            403: OpenApiResponse(description="Non autorise"),
        },
    )
    def get(self, request: Request, module: str) -> Response | FileResponse:
        """Telecharge directement le fichier d'export."""
        logger.info(
            "Export download request: module=%s, user=%s, authenticated=%s",
            module,
            getattr(request.user, "id", "anonymous"),
            request.user.is_authenticated if hasattr(request.user, "is_authenticated") else False,
        )

        export_format = request.query_params.get("export_format", "json")
        filters = {k: v for k, v in request.query_params.items() if k != "export_format"}

        try:
            job = ExporterService.create_export_job(
                user=request.user,
                module=module,
                export_format=export_format,
                filters=filters if filters else None,
            )

            if job.status == ExportJob.Status.COMPLETED and job.file:
                content_types = {
                    "json": "application/json",
                    "csv": "text/csv",
                    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                }
                file_name = job.file.name.split("/")[-1] if job.file.name else "export"
                response = FileResponse(
                    job.file.open("rb"),
                    as_attachment=True,
                    filename=file_name,
                    content_type=content_types.get(export_format, "application/octet-stream"),
                )
                # xlsx est deja compresse: identity evite double-compression par GZipMiddleware.
                if export_format == "xlsx":
                    response["Content-Encoding"] = "identity"
                return response

            return Response(
                {"error": job.error_message or "Export echoue"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except ValueError as e:
            logger.warning("Export error for module %s: %s", module, str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (DatabaseError, OperationalError):
            logger.exception("Database error during export download")
            return Response(
                {"error": "Erreur lors de l'export"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExportBulkView(APIView):
    """Vue pour l'export bulk de plusieurs modules dans un ZIP."""

    permission_classes = [IsAdminUser]
    throttle_classes = [ExportThrottle]

    @extend_schema(
        description="Export bulk de plusieurs modules dans un fichier ZIP",
        parameters=[
            OpenApiParameter(
                "modules",
                location=OpenApiParameter.QUERY,
                description="Liste de modules separes par virgule (ex: articles,projects) ou 'all'",
                type=str,
                default="all",
            ),
            OpenApiParameter(
                "export_format",
                location=OpenApiParameter.QUERY,
                description="Format d'export pour les fichiers dans le ZIP (json, csv, xlsx)",
                type=str,
                default="json",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Fichier ZIP contenant les exports"),
            400: OpenApiResponse(description="Requete invalide"),
        },
    )
    def get(self, request: Request) -> Response | HttpResponse:
        """Exporte plusieurs modules dans un fichier ZIP."""
        export_format = request.query_params.get("export_format", "json")
        modules_param = request.query_params.get("modules", "all")

        logger.info(
            "=== ExportBulkView: modules_param=%s, export_format=%s ===",
            modules_param,
            export_format,
        )

        if modules_param.lower() == "all":
            module_list = ["articles", "projects", "stacks", "experiences"]
        else:
            module_list = [m.strip().lower() for m in modules_param.split(",") if m.strip()]

        if not module_list:
            return Response(
                {"error": "Aucun module specifie"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info("Modules a exporter: %s", module_list)

        try:
            zip_content, module_counts = ExporterService.export_multiple_to_zip(
                modules=module_list,
                export_format=export_format,
            )

            logger.info(
                "ZIP genere: %d bytes, module_counts=%s",
                len(zip_content) if zip_content else 0,
                module_counts,
            )

            successful_exports = {k: v for k, v in module_counts.items() if v >= 0}
            if not successful_exports:
                logger.error("Aucun export reussi parmi: %s", module_counts)
                return Response(
                    {"error": "Aucun module n'a pu etre exporte"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # ZIP header minimal = 22 bytes (EOCD) => en dessous, archive invalide.
            if not zip_content or len(zip_content) < 22:
                logger.error("ZIP vide ou trop petit: %d bytes", len(zip_content) if zip_content else 0)
                return Response(
                    {"error": "Le fichier ZIP genere est vide"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_bulk_{timestamp}.zip"

            logger.info(
                "=== Envoi ZIP: filename=%s, size=%d bytes ===",
                filename,
                len(zip_content),
            )

            # identity empeche GZipMiddleware de re-compresser un ZIP deja compresse.
            response = HttpResponse(
                content=zip_content,
                content_type="application/zip",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            response["Content-Length"] = str(len(zip_content))
            response["Content-Encoding"] = "identity"
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

        except (DatabaseError, OperationalError):
            logger.exception("Erreur DB lors de l'export bulk")
            return Response(
                {"errors": [{"code": "export_error", "message": "Erreur lors de l'export."}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception:
            logger.exception("Erreur inattendue lors de l'export bulk")
            return Response(
                {"errors": [{"code": "internal_error", "message": "Erreur inattendue."}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
