"""Vues pour les experiences professionnelles."""

import logging

from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet
from utils.exceptions.service import NotFoundError
from utils.pagination import APIResponsePagination

from ..doc import EXPERIENCE_LIST_PARAMS, RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_EXPERIENCES
from ..filters import ExperienceFilter
from ..models import Experience
from ..serializers import ExperienceSerializer, ExperienceWriteSerializer
from ..services import ExperienceService
from ..throttles import ExperienceThrottle

logger = logging.getLogger("core.experiences")


class ExperienceViewSet(BaseAPIViewSet):
    """API endpoint pour les experiences professionnelles."""

    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (ExperienceThrottle,)
    pagination_class = APIResponsePagination
    filterset_class = ExperienceFilter
    lookup_field = "pk"

    serializer_classes = {
        "write": ExperienceWriteSerializer,
    }

    def _get_base_queryset(self) -> QuerySet[Experience]:
        """Retourne les experiences avec relations pre-chargees."""
        return Experience.objects.with_related()

    @swagger_auto_schema(
        operation_summary="Liste des experiences",
        operation_description="Recupere la liste des experiences avec filtres optionnels.",
        manual_parameters=EXPERIENCE_LIST_PARAMS,
        responses={200: ExperienceSerializer(many=True)},
        tags=TAGS_EXPERIENCES,
    )
    def list(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Liste des experiences."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Details d'une experience",
        operation_description="Recupere les details d'une experience par son ID.",
        responses={200: ExperienceSerializer(), 404: RESPONSE_404},
        tags=TAGS_EXPERIENCES,
    )
    def retrieve(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Details d'une experience."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creer une experience",
        operation_description="Cree une nouvelle experience.",
        request_body=ExperienceSerializer,
        responses={201: ExperienceSerializer(), 400: RESPONSE_400},
        tags=TAGS_EXPERIENCES,
    )
    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Cree une experience."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Modifier une experience",
        operation_description="Met a jour completement une experience.",
        request_body=ExperienceSerializer,
        responses={200: ExperienceSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_EXPERIENCES,
    )
    def update(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Met a jour une experience."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Modifier partiellement une experience",
        operation_description="Met a jour partiellement une experience.",
        request_body=ExperienceSerializer,
        responses={200: ExperienceSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_EXPERIENCES,
    )
    def partial_update(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Met a jour partiellement une experience."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer une experience",
        operation_description="Supprime une experience existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_EXPERIENCES,
    )
    def destroy(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Supprime une experience."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Experiences par type",
        operation_description="Recupere les experiences d'un type specifique.",
        responses={200: ExperienceSerializer(many=True), 404: RESPONSE_404},
        tags=TAGS_EXPERIENCES,
    )
    @action(detail=False, methods=["get"], url_path="by-type/(?P<type_name>[^/.]+)")
    def by_type(self, _request: Request, type_name: str = "") -> Response:
        """Experiences par type."""
        experiences = ExperienceService.get_by_type(type_name)
        return self.paginated_response(experiences)

    @swagger_auto_schema(
        operation_summary="Experience en cours",
        operation_description="Recupere l'experience en cours (sans date de fin).",
        responses={200: ExperienceSerializer(), 404: RESPONSE_404},
        tags=TAGS_EXPERIENCES,
    )
    @action(detail=False, methods=["get"])
    def current(self, _request: Request) -> Response:
        """Experience en cours."""
        experience = ExperienceService.get_current()
        if not experience:
            raise NotFoundError("Aucune experience en cours.")

        serializer = self.get_serializer(experience)
        return Response(serializer.data)
