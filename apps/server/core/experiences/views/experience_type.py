"""Vues pour les types d'experiences."""

from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..doc import RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_TYPES
from ..models import ExperienceType
from ..serializers import ExperienceTypeSerializer
from ..throttles import ExperienceThrottle


class ExperienceTypeViewSet(BaseAPIViewSet):
    """API endpoint pour les types d'experiences."""

    queryset = ExperienceType.objects.all()
    serializer_class = ExperienceTypeSerializer
    throttle_classes = [ExperienceThrottle]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Liste des types d'experiences",
        operation_description="Recupere tous les types d'experiences.",
        responses={200: ExperienceTypeSerializer(many=True)},
        tags=TAGS_TYPES,
    )
    @method_decorator(cache_page(1800))
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Liste des types."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Details d'un type",
        operation_description="Recupere un type d'experience par son ID.",
        responses={200: ExperienceTypeSerializer(), 404: RESPONSE_404},
        tags=TAGS_TYPES,
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Details d'un type."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creer un type",
        operation_description="Cree un nouveau type d'experience.",
        request_body=ExperienceTypeSerializer,
        responses={201: ExperienceTypeSerializer(), 400: RESPONSE_400},
        tags=TAGS_TYPES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree un type."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Modifier un type",
        operation_description="Met a jour completement un type d'experience.",
        request_body=ExperienceTypeSerializer,
        responses={200: ExperienceTypeSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_TYPES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour un type."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Modifier partiellement un type",
        operation_description="Met a jour partiellement un type d'experience.",
        request_body=ExperienceTypeSerializer,
        responses={200: ExperienceTypeSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_TYPES,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement un type."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer un type",
        operation_description="Supprime un type d'experience.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_TYPES,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime un type."""
        return super().destroy(request, *args, **kwargs)
