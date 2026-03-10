"""Vues pour les informations de contact."""

import logging
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..doc import RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_INFO
from ..models import ContactInfo
from ..serializers import ContactInfoSerializer
from ..services import ContactInfoService
from ..throttles import ContactsThrottle

logger = logging.getLogger(__name__)


class ContactInfoViewSet(BaseAPIViewSet):
    """API endpoint pour les informations de contact."""

    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    throttle_classes = [ContactsThrottle]

    @swagger_auto_schema(
        operation_summary="Liste des informations de contact",
        operation_description="Recupere les informations de contact.",
        responses={200: ContactInfoSerializer(many=True)},
        tags=TAGS_INFO,
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Liste les informations de contact."""
        if not request.user.is_authenticated:
            result = ContactInfoService.get_public_info()
            if result is None:
                return Response([])
            if isinstance(result, dict):
                return Response([result])
            serializer = self.get_serializer(result)
            return Response([serializer.data])
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Details d'une information de contact",
        operation_description="Recupere les details d'une information de contact.",
        responses={200: ContactInfoSerializer(), 404: RESPONSE_404},
        tags=TAGS_INFO,
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'une information de contact."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creer une information de contact",
        operation_description="Cree une nouvelle information de contact.",
        request_body=ContactInfoSerializer,
        responses={201: ContactInfoSerializer(), 400: RESPONSE_400},
        tags=TAGS_INFO,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une nouvelle information de contact."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour une information de contact",
        operation_description="Met a jour une information de contact existante.",
        request_body=ContactInfoSerializer,
        responses={200: ContactInfoSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_INFO,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une information de contact."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour partiellement une information de contact",
        operation_description="Met a jour partiellement une information de contact.",
        request_body=ContactInfoSerializer,
        responses={200: ContactInfoSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_INFO,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une information de contact."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer une information de contact",
        operation_description="Supprime une information de contact existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_INFO,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une information de contact."""
        return super().destroy(request, *args, **kwargs)
