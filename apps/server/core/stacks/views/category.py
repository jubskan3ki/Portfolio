"""Views pour les categories de stacks."""

from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
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

    @extend_schema(
        summary="Liste des categories",
        description="Recupere toutes les categories de stacks.",
        responses={200: StackCategorySerializer(many=True)},
        tags=TAGS_CATEGORIES,
    )
    @method_decorator(cache_page(1800))
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Liste des categories."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Details d'une categorie",
        description="Recupere une categorie par son nom.",
        responses={200: StackCategorySerializer, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Details d'une categorie."""
        name = kwargs.get("name", "")
        instance = CategoryService.get_by_name(name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Creer une categorie",
        description="Cree une nouvelle categorie.",
        request=StackCategorySerializer,
        responses={201: StackCategorySerializer, 400: RESPONSE_400},
        tags=TAGS_CATEGORIES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une categorie."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier une categorie",
        description="Met a jour completement une categorie.",
        request=StackCategorySerializer,
        responses={200: StackCategorySerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une categorie."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier partiellement une categorie",
        description="Met a jour partiellement une categorie.",
        request=StackCategorySerializer,
        responses={200: StackCategorySerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une categorie."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer une categorie",
        description="Supprime une categorie existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une categorie."""
        return super().destroy(request, *args, **kwargs)
