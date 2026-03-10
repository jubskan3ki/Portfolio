"""Vues pour les projets."""

from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet, parse_limit
from utils.pagination import APIResponsePagination

from ..doc import (
    PAGINATION_PARAMS,
    PARAM_FEATURED_LIMIT,
    PROJECT_LIST_PARAMS,
    RESPONSE_200_LIST,
    RESPONSE_204,
    RESPONSE_400,
    RESPONSE_404,
    TAGS_PROJECTS,
)
from ..filters import ProjectFilter
from ..models import Project
from ..serializers.project import ProjectDetailSerializer, ProjectListSerializer, ProjectWriteSerializer
from ..services.interaction import InteractionService
from ..services.project import ProjectService
from ..throttles import ProjectsThrottle, ProjectViewThrottle


class ProjectViewSet(BaseAPIViewSet):
    """API endpoint pour les projets."""

    queryset = Project.objects.select_related("category", "status")
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [ProjectsThrottle]
    pagination_class = APIResponsePagination
    filterset_class = ProjectFilter
    lookup_field = "slug"

    # Configuration pour SerializerByActionMixin
    serializer_classes = {
        "list": ProjectListSerializer,
        "featured": ProjectListSerializer,
        "by_category": ProjectListSerializer,
        "create": ProjectWriteSerializer,
        "update": ProjectWriteSerializer,
        "partial_update": ProjectWriteSerializer,
    }

    @swagger_auto_schema(
        operation_summary="Liste des projets",
        operation_description="Recupere la liste des projets, filtrable par differents criteres.",
        manual_parameters=PROJECT_LIST_PARAMS,
        responses={200: RESPONSE_200_LIST},
        tags=TAGS_PROJECTS,
    )
    def list(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Recupere la liste des projets."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Details d'un projet",
        operation_description="Recupere les details d'un projet par son slug ou ID.",
        responses={200: ProjectDetailSerializer(), 404: RESPONSE_404},
        tags=TAGS_PROJECTS,
    )
    def retrieve(self, _request: Request, *_args: object, **_kwargs: object) -> Response:
        """Recupere les details d'un projet par son slug ou ID."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Creer un projet",
        operation_description="Cree un nouveau projet.",
        request_body=ProjectWriteSerializer,
        responses={201: ProjectListSerializer(), 400: RESPONSE_400},
        tags=TAGS_PROJECTS,
    )
    def create(self, request: Request, *_args: object, **_kwargs: object) -> Response:
        """Cree un nouveau projet."""
        return self.write_with_response_serializer(request, ProjectListSerializer)

    @swagger_auto_schema(
        operation_summary="Mettre a jour un projet",
        operation_description="Met a jour completement un projet existant.",
        request_body=ProjectWriteSerializer,
        responses={200: ProjectListSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_PROJECTS,
    )
    def update(self, request: Request, *_args: object, **_kwargs: object) -> Response:
        """Met a jour completement un projet existant."""
        return self.write_with_response_serializer(request, ProjectListSerializer, instance=self.get_object())

    @swagger_auto_schema(
        operation_summary="Mettre a jour partiellement un projet",
        operation_description="Met a jour partiellement un projet existant.",
        request_body=ProjectWriteSerializer,
        responses={200: ProjectListSerializer(), 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_PROJECTS,
    )
    def partial_update(self, request: Request, *_args: object, **_kwargs: object) -> Response:
        """Met a jour partiellement un projet existant."""
        return self.write_with_response_serializer(
            request, ProjectListSerializer, instance=self.get_object(), partial=True
        )

    @swagger_auto_schema(
        operation_summary="Supprimer un projet",
        operation_description="Supprime un projet existant.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_PROJECTS,
    )
    def destroy(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Supprime un projet existant."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Projets par categorie",
        operation_description="Recupere les projets d'une categorie specifique.",
        manual_parameters=PAGINATION_PARAMS,
        responses={200: RESPONSE_200_LIST, 404: RESPONSE_404},
        tags=TAGS_PROJECTS,
    )
    @action(detail=False, methods=["get"], url_path="by-category/(?P<category_slug>[^/.]+)")
    def by_category(self, _request: Request, category_slug: str | None = None) -> Response:
        """Recupere les projets par categorie."""
        queryset = ProjectService.get_by_category(category_slug or "")
        return self.paginated_response(queryset, ProjectListSerializer)

    @swagger_auto_schema(
        operation_summary="Projets mis en avant",
        operation_description="Recupere les projets mis en avant (les plus aimes).",
        manual_parameters=[PARAM_FEATURED_LIMIT],
        responses={200: ProjectListSerializer(many=True)},
        tags=TAGS_PROJECTS,
    )
    @action(detail=False, methods=["get"])
    def featured(self, request: Request) -> Response:
        """Recupere les projets mis en avant."""
        limit = parse_limit(request.query_params.get("limit"), default=3)
        projects = ProjectService.get_featured(limit)
        serializer = ProjectListSerializer(projects, many=True, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Incrementer les vues d'un projet",
        operation_description="Incremente le compteur de vues d'un projet.",
        responses={200: ProjectDetailSerializer(), 404: RESPONSE_404},
        tags=TAGS_PROJECTS,
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        throttle_classes=[ProjectViewThrottle],
    )
    def view(self, _request: Request, slug: str | None = None) -> Response:
        """Incremente le compteur de vues d'un projet."""
        project = InteractionService.increment_view_and_get(slug or "")
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def _get_base_queryset(self) -> QuerySet[Project]:
        """Retourne les projets avec relations pre-chargees."""
        return Project.objects.select_related("category", "status")
