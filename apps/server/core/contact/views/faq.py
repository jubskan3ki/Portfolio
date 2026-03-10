"""Vues pour les FAQs."""

from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet
from utils.pagination import APIResponsePagination

from ..doc import RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_FAQ
from ..models import FAQ
from ..serializers import FAQSerializer
from ..services import FAQService
from ..throttles import ContactsThrottle


class FAQViewSet(BaseAPIViewSet):
    """API endpoint pour les questions frequemment posees."""

    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    throttle_classes = [ContactsThrottle]
    pagination_class = APIResponsePagination

    @swagger_auto_schema(
        operation_summary="Liste des FAQs",
        operation_description="Recupere la liste des FAQs publiees.",
        responses={200: FAQSerializer(many=True)},
        tags=TAGS_FAQ,
    )
    def list(self, request: Request, *_args: Any, **_kwargs: Any) -> Response:
        """Liste les FAQs publiees."""
        published_only = not request.user.is_authenticated
        queryset = FAQService.get_all(published_only=published_only)
        return self.paginated_response(queryset)

    @swagger_auto_schema(
        operation_summary="Details d'une FAQ",
        operation_description="Recupere les details d'une FAQ par son ID.",
        responses={200: FAQSerializer(), 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'une FAQ."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creer une FAQ",
        operation_description="Cree une nouvelle FAQ.",
        request_body=FAQSerializer,
        responses={201: FAQSerializer(), 400: RESPONSE_400},
        tags=TAGS_FAQ,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une nouvelle FAQ."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour une FAQ",
        operation_description="Met a jour une FAQ existante.",
        request_body=FAQSerializer,
        responses={200: FAQSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une FAQ existante."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour partiellement une FAQ",
        operation_description="Met a jour partiellement une FAQ existante.",
        request_body=FAQSerializer,
        responses={200: FAQSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une FAQ existante."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer une FAQ",
        operation_description="Supprime une FAQ existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une FAQ existante."""
        return super().destroy(request, *args, **kwargs)
