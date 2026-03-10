"""Views pour les categories de stacks."""

from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..doc import RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_CATEGORIES
from ..models import StackCategory
from ..serializers import StackCategorySerializer
from ..services import CategoryService
from ..throttles import StacksThrottle


class CategoryViewSet(BaseAPIViewSet):
    """API endpoint pour les categories de stacks."""

    queryset = StackCategory.objects.all()
    serializer_class = StackCategorySerializer
    throttle_classes = [StacksThrottle]
    lookup_field = "name"

    def _get_base_queryset(self):
        """Retourne les categories avec comptage."""
        return CategoryService.get_all(with_count=True)

    @swagger_auto_schema(
        operation_summary="Liste des categories",
        operation_description="Recupere toutes les categories de stacks.",
        responses={200: StackCategorySerializer(many=True)},
        tags=TAGS_CATEGORIES,
    )
    @method_decorator(cache_page(1800))
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Liste des categories."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Details d'une categorie",
        operation_description="Recupere une categorie par son nom.",
        responses={200: StackCategorySerializer(), 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, _request: Request, *_args: Any, **kwargs: Any) -> Response:
        """Details d'une categorie."""
        name = kwargs.get("name", "")
        instance = CategoryService.get_by_name(name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Creer une categorie",
        operation_description="Cree une nouvelle categorie.",
        request_body=StackCategorySerializer,
        responses={201: StackCategorySerializer(), 400: RESPONSE_400},
        tags=TAGS_CATEGORIES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une categorie."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Modifier une categorie",
        operation_description="Met a jour completement une categorie.",
        request_body=StackCategorySerializer,
        responses={200: StackCategorySerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une categorie."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Modifier partiellement une categorie",
        operation_description="Met a jour partiellement une categorie.",
        request_body=StackCategorySerializer,
        responses={200: StackCategorySerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une categorie."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer une categorie",
        operation_description="Supprime une categorie existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une categorie."""
        return super().destroy(request, *args, **kwargs)
