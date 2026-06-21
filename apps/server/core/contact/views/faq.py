"""Vues pour les FAQs."""

from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
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

    def _get_base_queryset(self) -> QuerySet[FAQ]:
        """Restreint aux FAQs publiees pour les anonymes (toutes actions, dont retrieve)."""
        published_only = not self.request.user.is_authenticated
        return FAQService.get_all(published_only=published_only)

    @extend_schema(
        summary="Liste des FAQs",
        description="Recupere la liste des FAQs publiees.",
        responses={200: FAQSerializer(many=True)},
        tags=TAGS_FAQ,
    )
    def list(self, request: Request, *_args: Any, **_kwargs: Any) -> Response:
        """Liste les FAQs publiees."""
        return self.paginated_response(self.get_queryset())

    @extend_schema(
        summary="Details d'une FAQ",
        description="Recupere les details d'une FAQ par son ID.",
        responses={200: FAQSerializer, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'une FAQ."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Creer une FAQ",
        description="Cree une nouvelle FAQ.",
        request=FAQSerializer,
        responses={201: FAQSerializer, 400: RESPONSE_400},
        tags=TAGS_FAQ,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une nouvelle FAQ."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour une FAQ",
        description="Met a jour une FAQ existante.",
        request=FAQSerializer,
        responses={200: FAQSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une FAQ existante."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour partiellement une FAQ",
        description="Met a jour partiellement une FAQ existante.",
        request=FAQSerializer,
        responses={200: FAQSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une FAQ existante."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer une FAQ",
        description="Supprime une FAQ existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_FAQ,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une FAQ existante."""
        return super().destroy(request, *args, **kwargs)
