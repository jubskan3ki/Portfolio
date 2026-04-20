"""Endpoint unifie de recherche full-text."""

from dataclasses import asdict

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import APIResponsePagination

from .serializers import SearchQuerySerializer, SearchResultSerializer
from .services import VALID_TYPES, SearchService
from .throttles import SearchThrottle


@extend_schema(
    tags=["Search"],
    summary="Recherche unifiee full-text",
    description=(
        "Recherche full-text PostgreSQL (tsvector + ranking) sur articles, projets, stacks "
        "et experiences. Les resultats sont tries par pertinence (rank desc) et incluent un "
        "extrait surligne via <mark>. Pour les articles, les non-publies ne sont visibles que "
        "pour les utilisateurs staff."
    ),
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            required=True,
            description="Terme de recherche (min 2 caracteres).",
        ),
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            enum=list(VALID_TYPES),
            required=False,
            description="Restreint la recherche a un type. 'all' par defaut.",
        ),
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            required=False,
            description="Numero de page (pagination standard).",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            required=False,
            description="Nombre de resultats par page (max 50).",
        ),
    ],
    responses={200: SearchResultSerializer(many=True)},
    examples=[
        OpenApiExample(
            "Recherche tous types",
            description="Requete typique multi-entite",
            value={
                "data": [
                    {
                        "type": "article",
                        "id": 7,
                        "slug": "demarrer-avec-django",
                        "title": "Demarrer avec Django",
                        "url": "/blog/demarrer-avec-django",
                        "rank": 0.892,
                        "snippet": "Guide complet pour <mark>Django</mark> 5...",
                        "metadata": {
                            "category": "Tutoriels",
                            "published_date": "2026-02-10T10:00:00Z",
                            "is_featured": False,
                        },
                    },
                ],
                "pagination": {"total": 1, "page": 1, "limit": 10, "totalPages": 1, "next": None, "previous": None},
            },
            response_only=True,
        ),
    ],
)
class SearchView(APIView):
    """GET /api/search/?q=<query>&type=<all|articles|projects|stacks|experiences>."""

    permission_classes = [AllowAny]
    throttle_classes = [SearchThrottle]
    pagination_class = APIResponsePagination

    def get(self, request: Request) -> Response:
        query_serializer = SearchQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        params = query_serializer.validated_data

        service = SearchService(
            query=params["q"],
            types=[params["type"]],
            user=request.user if request.user.is_authenticated else None,
        )
        results = [asdict(r) for r in service.run()]

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(results, request, view=self)
        if page is None:
            return Response({"data": results, "pagination": {}})
        return paginator.get_paginated_response(page)
