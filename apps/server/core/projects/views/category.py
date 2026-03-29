"""Vues pour les categories de projets."""

from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..doc import RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_CATEGORIES
from ..models import ProjectCategory
from ..serializers.category import ProjectCategorySerializer
from ..services.category import CategoryService
from ..throttles import ProjectsThrottle


class CategoryViewSet(BaseAPIViewSet):
    """API endpoint pour les categories de projets."""

    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    throttle_classes = [ProjectsThrottle]
    lookup_field = "slug"

    @extend_schema(
        summary="Liste des categories",
        description="Recupere la liste de toutes les categories de projets.",
        responses={200: ProjectCategorySerializer(many=True)},
        tags=TAGS_CATEGORIES,
    )
    @method_decorator(cache_page(1800))
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere la liste de toutes les categories."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Details d'une categorie",
        description="Recupere les details d'une categorie par son slug.",
        responses={200: ProjectCategorySerializer, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'une categorie par son slug."""
        slug = kwargs.get("slug", "")
        instance = CategoryService.get_by_slug(slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Creer une categorie",
        description="Cree une nouvelle categorie de projet.",
        request=ProjectCategorySerializer,
        responses={201: ProjectCategorySerializer, 400: RESPONSE_400},
        tags=TAGS_CATEGORIES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une nouvelle categorie."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour une categorie",
        description="Met a jour completement une categorie existante.",
        request=ProjectCategorySerializer,
        responses={200: ProjectCategorySerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_CATEGORIES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour completement une categorie."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour partiellement une categorie",
        description="Met a jour partiellement une categorie existante.",
        request=ProjectCategorySerializer,
        responses={200: ProjectCategorySerializer, 400: RESPONSE_400, 404: RESPONSE_404},
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

    def _get_base_queryset(self):
        """Retourne toutes les categories avec comptage."""
        return CategoryService.get_all(with_count=True)
