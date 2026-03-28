"""Vues pour les statuts de projets."""

from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
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

    @extend_schema(
        summary="Liste des statuts",
        description="Recupere la liste de tous les statuts de projets.",
        responses={200: ProjectStatusSerializer(many=True)},
        tags=TAGS_STATUSES,
    )
    @method_decorator(cache_page(1800))
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere la liste de tous les statuts."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Details d'un statut",
        description="Recupere les details d'un statut par son ID.",
        responses={200: ProjectStatusSerializer, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'un statut par son ID."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Creer un statut",
        description="Cree un nouveau statut de projet.",
        request=ProjectStatusSerializer,
        responses={201: ProjectStatusSerializer, 400: RESPONSE_400},
        tags=TAGS_STATUSES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree un nouveau statut."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour un statut",
        description="Met a jour completement un statut existant.",
        request=ProjectStatusSerializer,
        responses={200: ProjectStatusSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour completement un statut."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour partiellement un statut",
        description="Met a jour partiellement un statut existant.",
        request=ProjectStatusSerializer,
        responses={200: ProjectStatusSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement un statut."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer un statut",
        description="Supprime un statut existant.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_STATUSES,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime un statut."""
        return super().destroy(request, *args, **kwargs)
