"""Vues pour les statuts de projets."""

from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..doc import RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_STATUSES
from ..models import ProjectStatus
from ..serializers.status import ProjectStatusSerializer
from ..throttles import ProjectsThrottle


class StatusViewSet(BaseAPIViewSet):
    """API endpoint pour les statuts de projets."""

    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusSerializer
    throttle_classes = [ProjectsThrottle]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Liste des statuts",
        operation_description="Recupere la liste de tous les statuts de projets.",
        responses={200: ProjectStatusSerializer(many=True)},
        tags=TAGS_STATUSES,
    )
    @method_decorator(cache_page(1800))
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere la liste de tous les statuts."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Details d'un statut",
        operation_description="Recupere les details d'un statut par son ID.",
        responses={200: ProjectStatusSerializer(), 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'un statut par son ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creer un statut",
        operation_description="Cree un nouveau statut de projet.",
        request_body=ProjectStatusSerializer,
        responses={201: ProjectStatusSerializer(), 400: RESPONSE_400},
        tags=TAGS_STATUSES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree un nouveau statut."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour un statut",
        operation_description="Met a jour completement un statut existant.",
        request_body=ProjectStatusSerializer,
        responses={200: ProjectStatusSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour completement un statut."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour partiellement un statut",
        operation_description="Met a jour partiellement un statut existant.",
        request_body=ProjectStatusSerializer,
        responses={200: ProjectStatusSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement un statut."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer un statut",
        operation_description="Supprime un statut existant.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime un statut."""
        return super().destroy(request, *args, **kwargs)
