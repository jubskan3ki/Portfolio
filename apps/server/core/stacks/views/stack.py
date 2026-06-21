"""Views pour les stacks techniques."""

from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.articles.serializers import ArticleListSerializer
from core.projects.serializers import ProjectListSerializer
from utils.api import BaseAPIViewSet
from utils.pagination import APIResponsePagination

from ..doc import RESPONSE_400, RESPONSE_404, STACK_LIST_PARAMS, TAGS_STACKS
from ..filters import StackFilter
from ..models import Stack
from ..serializers import (
    RelatedStackSerializer,
    StackDetailSerializer,
    StackListSerializer,
    StackWriteSerializer,
)
from ..services.stack import StackService
from ..throttles import StacksThrottle


class StackViewSet(BaseAPIViewSet):
    """API endpoint pour les stacks techniques."""

    queryset = Stack.objects.all()
    serializer_class = StackDetailSerializer
    # Permissions gérées par AdminWritePermissionMixin : lecture publique,
    # écriture réservée à l'admin (get_permissions).
    throttle_classes = (StacksThrottle,)
    pagination_class = APIResponsePagination
    filterset_class = StackFilter
    lookup_field = "slug"

    serializer_classes = {
        "list": StackListSerializer,
        "by_category": StackListSerializer,
        "create": StackWriteSerializer,
        "update": StackWriteSerializer,
        "partial_update": StackWriteSerializer,
        "projects": ProjectListSerializer,
        "articles": ArticleListSerializer,
    }

    def _get_base_queryset(self) -> QuerySet[Stack]:
        """Queryset adapte a l'action : prefetch lourd seulement pour le detail."""
        if self.action == "retrieve":
            return Stack.objects.with_detail()
        return Stack.objects.with_related()

    @extend_schema(
        summary="Liste des stacks",
        description="Recupere la liste des stacks techniques avec filtres optionnels.",
        parameters=STACK_LIST_PARAMS,
        responses={200: StackListSerializer(many=True)},
        tags=TAGS_STACKS,
    )
    def list(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Liste des stacks."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Details d'une stack",
        description="Recupere les details d'une stack par son slug ou ID.",
        responses={200: StackDetailSerializer, 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Details d'une stack."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Creer une stack",
        description="Cree une nouvelle stack technique.",
        request=StackWriteSerializer,
        responses={201: StackDetailSerializer, 400: RESPONSE_400},
        tags=TAGS_STACKS,
    )
    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Cree une stack."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier une stack",
        description="Met a jour completement une stack.",
        request=StackWriteSerializer,
        responses={200: StackDetailSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    def update(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Met a jour une stack."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier partiellement une stack",
        description="Met a jour partiellement une stack.",
        request=StackWriteSerializer,
        responses={200: StackDetailSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    def partial_update(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Met a jour partiellement une stack."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer une stack",
        description="Supprime une stack existante.",
        responses={204: OpenApiResponse(description="Supprime avec succes"), 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    def destroy(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Supprime une stack."""
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Stacks par categorie",
        description="Recupere les stacks d'une categorie specifique.",
        responses={200: StackListSerializer(many=True), 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    @action(detail=False, methods=["get"], url_path="by-category/(?P<category_name>[^/.]+)")
    def by_category(self, _request: Request, category_name: str = "") -> Response:
        """Stacks par categorie."""
        stacks = StackService.get_by_category(category_name)
        return self.paginated_response(stacks, StackListSerializer)

    @extend_schema(
        summary="Stacks associees",
        description="Recupere les stacks associees a une stack.",
        responses={
            200: OpenApiResponse(description="Liste des stacks associees"),
            404: RESPONSE_404,
        },
        tags=TAGS_STACKS,
    )
    @action(detail=True, methods=["get"])
    def related(self, _request: Request, slug: str = "") -> Response:
        """Stacks associees."""
        stack = StackService.get_by_slug(slug)
        related_stacks, relationship_map = StackService.get_related(stack)
        serializer = RelatedStackSerializer(
            related_stacks,
            many=True,
            context={"relationships": relationship_map},
        )
        return Response(serializer.data)

    @extend_schema(
        summary="Projets utilisant cette stack",
        description="Recupere les projets qui utilisent cette technologie.",
        responses={200: ProjectListSerializer(many=True), 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    @action(detail=True, methods=["get"])
    def projects(self, _request: Request, slug: str = "") -> Response:
        """Projets utilisant cette stack."""
        stack = StackService.get_by_slug(slug)
        projects_qs = StackService.get_projects_for_stack(stack)
        return self.paginated_response(projects_qs, ProjectListSerializer)

    @extend_schema(
        summary="Articles lies a cette stack",
        description="Recupere les articles de blog lies a cette technologie.",
        responses={200: ArticleListSerializer(many=True), 404: RESPONSE_404},
        tags=TAGS_STACKS,
    )
    @action(detail=True, methods=["get"])
    def articles(self, _request: Request, slug: str = "") -> Response:
        """Articles lies a cette stack."""
        stack = StackService.get_by_slug(slug)
        articles_qs = StackService.get_articles_for_stack(stack)
        return self.paginated_response(articles_qs, ArticleListSerializer)
