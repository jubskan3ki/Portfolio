"""Views pour la gestion des jobs."""

from datetime import timedelta
from typing import TYPE_CHECKING, cast

from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import ExportJob, ImportJob
from ..serializers import ExportJobSerializer, ImportJobSerializer

if TYPE_CHECKING:
    from core.user.models import User as AppUser


class JobViewSet(viewsets.ViewSet):
    """ViewSet pour consulter les jobs d'import/export."""

    permission_classes = [IsAdminUser]

    @extend_schema(
        description="Liste tous les jobs de l'utilisateur",
        responses={200: OpenApiResponse(description="Liste des jobs")},
    )
    def list(self, request: Request) -> Response:
        """Liste tous les jobs de l'utilisateur."""
        export_jobs = ExportJob.objects.filter(user=cast("AppUser", request.user)).order_by("-created_at")[:20]
        import_jobs = ImportJob.objects.filter(user=cast("AppUser", request.user)).order_by("-created_at")[:20]

        return Response(
            {
                "exports": ExportJobSerializer(export_jobs, many=True, context={"request": request}).data,
                "imports": ImportJobSerializer(import_jobs, many=True).data,
            }
        )

    @extend_schema(
        description="Detail d'un job d'export",
        responses={200: ExportJobSerializer, 404: OpenApiResponse(description="Job non trouve")},
    )
    def export_detail(self, request: Request, job_id: str) -> Response:
        """Detail d'un job d'export."""
        try:
            job = ExportJob.objects.get(id=job_id, user=cast("AppUser", request.user))
            return Response(ExportJobSerializer(job, context={"request": request}).data)
        except ExportJob.DoesNotExist:
            return Response(
                {"error": "Job non trouve"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        description="Detail d'un job d'import",
        responses={200: ImportJobSerializer, 404: OpenApiResponse(description="Job non trouve")},
    )
    def import_detail(self, request: Request, job_id: str) -> Response:
        """Detail d'un job d'import."""
        try:
            job = ImportJob.objects.get(id=job_id, user=cast("AppUser", request.user))
            return Response(ImportJobSerializer(job).data)
        except ImportJob.DoesNotExist:
            return Response(
                {"error": "Job non trouve"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        description="Supprime les anciens jobs",
        responses={200: OpenApiResponse(description="Jobs supprimes")},
    )
    def cleanup(self, request: Request) -> Response:
        """Supprime les anciens jobs de l'utilisateur."""

        cutoff = timezone.now() - timedelta(days=7)

        export_deleted, _ = ExportJob.objects.filter(
            user=cast("AppUser", request.user),
            created_at__lt=cutoff,
        ).delete()

        import_deleted, _ = ImportJob.objects.filter(
            user=cast("AppUser", request.user),
            created_at__lt=cutoff,
        ).delete()

        return Response(
            {
                "deleted": {
                    "exports": export_deleted,
                    "imports": import_deleted,
                }
            }
        )
