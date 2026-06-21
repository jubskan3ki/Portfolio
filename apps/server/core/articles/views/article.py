"""Vues pour les articles avec CRUD complet et actions supplementaires."""

from typing import Any

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet, parse_limit
from utils.cache.keys import CacheKeys
from utils.pagination import APIResponsePagination

from ..doc import (
    PARAM_LIMIT,
    PARAMS_LIST,
    PARAMS_PAGINATION,
    RESPONSE_200_ARTICLES,
    RESPONSE_204,
    RESPONSE_400,
    RESPONSE_404,
    TAGS_ARTICLES,
)
from ..filters import ArticleFilter
from ..models import Article
from ..serializers.article import ArticleDetailSerializer, ArticleListSerializer, ArticleWriteSerializer
from ..services.article import ArticleService
from ..throttles import ArticlesThrottle, ArticleViewThrottle


class ArticleViewSet(BaseAPIViewSet):
    """API endpoint pour les articles."""

    queryset = Article.objects.published_with_related()
    serializer_class = ArticleDetailSerializer
    throttle_classes = [ArticlesThrottle]
    pagination_class = APIResponsePagination
    filterset_class = ArticleFilter
    lookup_field = "slug"

    serializer_classes = {
        "list": ArticleListSerializer,
        "featured": ArticleListSerializer,
        "popular": ArticleListSerializer,
        "by_category": ArticleListSerializer,
        "by_tag": ArticleListSerializer,
        "create": ArticleWriteSerializer,
        "update": ArticleWriteSerializer,
        "partial_update": ArticleWriteSerializer,
    }

    @extend_schema(
        summary="Liste des articles",
        description="Recupere la liste des articles, filtrable par differents criteres.",
        parameters=PARAMS_LIST,
        responses={200: RESPONSE_200_ARTICLES},
        tags=TAGS_ARTICLES,
    )
    @method_decorator(
        cache_page(
            CacheKeys.TTL_MEDIUM,
            key_prefix="portfolio:v1:views:articles:list",
        )
    )
    def list(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Recupere la liste des articles."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Details d'un article",
        description="Recupere les details d'un article par son slug ou ID.",
        responses={200: ArticleDetailSerializer, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    @method_decorator(
        cache_page(
            CacheKeys.TTL_MEDIUM,
            key_prefix="portfolio:v1:views:articles:detail",
        )
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'un article par son slug ou ID."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Creer un article",
        description="Cree un nouvel article.",
        request=ArticleWriteSerializer,
        responses={201: ArticleDetailSerializer, 400: RESPONSE_400},
        tags=TAGS_ARTICLES,
    )
    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Cree un nouvel article (admin uniquement)."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour un article",
        description="Met a jour un article existant.",
        request=ArticleWriteSerializer,
        responses={200: ArticleDetailSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    def update(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Met a jour un article existant (admin uniquement)."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Mettre a jour partiellement un article",
        description="Met a jour partiellement un article existant.",
        request=ArticleWriteSerializer,
        responses={200: ArticleDetailSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    def partial_update(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Met a jour partiellement un article existant (admin uniquement)."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer un article",
        description="Supprime un article existant.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    def destroy(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Supprime un article existant (admin uniquement)."""
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Incrementer les vues d'un article",
        description="Incremente le compteur de vues d'un article.",
        responses={200: ArticleDetailSerializer, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        throttle_classes=[ArticleViewThrottle],
    )
    def view(self, _request: Request, slug: str | None = None) -> Response:
        """Incremente le compteur de vues d'un article."""
        article = ArticleService.increment_view_and_get(slug or "")
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    @extend_schema(
        summary="Articles mis en avant",
        description="Recupere les articles mis en avant.",
        parameters=[PARAM_LIMIT],
        responses={200: ArticleListSerializer(many=True)},
        tags=TAGS_ARTICLES,
    )
    @action(detail=False, methods=["get"])
    def featured(self, request: Request) -> Response:
        """Recupere les articles mis en avant."""
        limit = parse_limit(request.query_params.get("limit"))
        articles = ArticleService.get_featured(limit)
        serializer = ArticleListSerializer(articles, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        summary="Articles populaires",
        description="Recupere les articles les plus populaires.",
        parameters=[PARAM_LIMIT],
        responses={200: ArticleListSerializer(many=True)},
        tags=TAGS_ARTICLES,
    )
    @action(detail=False, methods=["get"])
    def popular(self, request: Request) -> Response:
        """Recupere les articles les plus populaires."""
        limit = parse_limit(request.query_params.get("limit"))
        articles = ArticleService.get_popular(limit)
        serializer = ArticleListSerializer(articles, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        summary="Articles lies",
        description="Recupere les articles similaires a cet article.",
        parameters=[PARAM_LIMIT],
        responses={200: ArticleListSerializer(many=True)},
        tags=TAGS_ARTICLES,
    )
    @action(detail=True, methods=["get"])
    def related(self, request: Request, slug: str | None = None) -> Response:
        """Recupere les articles similaires a cet article."""
        article = ArticleService.get_by_slug(slug or "")
        limit = parse_limit(request.query_params.get("limit"), default=3)
        related_articles = ArticleService.get_related(article, limit)
        serializer = ArticleListSerializer(related_articles, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        summary="Articles par categorie",
        description="Recupere les articles d'une categorie specifique.",
        parameters=PARAMS_PAGINATION,
        responses={200: RESPONSE_200_ARTICLES, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    @action(detail=False, methods=["get"], url_path="by-category/(?P<category_slug>[^/.]+)")
    def by_category(self, _request: Request, category_slug: str | None = None) -> Response:
        """Recupere les articles par categorie."""
        queryset = ArticleService.get_by_category(category_slug or "")
        return self.paginated_response(queryset, ArticleListSerializer)

    @extend_schema(
        summary="Articles par tag",
        description="Recupere les articles avec un tag specifique.",
        parameters=PARAMS_PAGINATION,
        responses={200: RESPONSE_200_ARTICLES, 404: RESPONSE_404},
        tags=TAGS_ARTICLES,
    )
    @action(detail=False, methods=["get"], url_path="by-tag/(?P<tag_name>[^/.]+)")
    def by_tag(self, _request: Request, tag_name: str | None = None) -> Response:
        """Recupere les articles par tag."""
        queryset = ArticleService.get_by_tag(tag_name or "")
        return self.paginated_response(queryset, ArticleListSerializer)

    def _get_base_queryset(self) -> QuerySet[Article]:
        """Retourne les articles avec relations pre-chargees.

        Staff en ecriture ou avec ?all=true: tous les articles.
        Sinon: uniquement les articles publies.
        """
        if self.request.user.is_staff and (
            self.action in ("retrieve", "update", "partial_update", "destroy")
            or self.request.query_params.get("all") == "true"
        ):
            return Article.objects.select_with_related()
        return Article.objects.published_with_related()
