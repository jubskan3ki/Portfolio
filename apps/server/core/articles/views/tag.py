"""Vues pour les tags d'articles."""

from typing import Any

from django.db.models import Count, Q, QuerySet, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..models import Tag
from ..serializers.tag import TagSerializer
from ..services.tag import TagService
from ..throttles import ArticlesThrottle


class TagViewSet(BaseAPIViewSet):
    """
    API endpoint pour les tags d'articles.

    Hérite de BaseAPIViewSet :
    - Permissions admin pour écriture (AdminWritePermissionMixin)
    - Logging automatique des actions CRUD (LoggingMixin)
    - Lookup par slug ou pk (SlugOrPkLookupMixin)
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    throttle_classes = [ArticlesThrottle]
    lookup_field = "name"
    # Liste complete renvoyee sans pagination (consommee en sidebar/admin-select).
    pagination_class = None

    serializer_classes = {
        "list": TagSerializer,
        "detail": TagSerializer,
        "write": TagSerializer,
    }

    def get_queryset(self) -> QuerySet[Tag]:
        """Filtre + ordonne les tags selon l'action.

        - list/retrieve: annote published_count et view_count_sum.
        - Public: exclut les tags sans article publie (published_count > 0).
        - list: tri par view_count_sum DESC, puis published_count DESC, puis name.
        - Query params ?category=<slug>&search=<str>: restreint le comptage aux
          articles qui matchent ces filtres, puis exclut les tags qui tombent a
          count=0 (le frontend n'affiche que des options encore pertinentes).
        """
        qs = super().get_queryset()
        if self.action in ("list", "retrieve"):
            now = timezone.now()
            published_filter = Q(articles__is_published=True, articles__published_date__lte=now)

            if self.action == "list":
                category = self.request.query_params.get("category")
                if category:
                    category_filter = Q(articles__category__slug=category)
                    if category.isdigit():
                        category_filter |= Q(articles__category_id=int(category))
                    published_filter &= category_filter
                search = self.request.query_params.get("search")
                if search:
                    published_filter &= (
                        Q(articles__title__icontains=search)
                        | Q(articles__excerpt__icontains=search)
                        | Q(articles__content__icontains=search)
                    )

            qs = qs.annotate(
                published_count=Count("articles", filter=published_filter, distinct=True),
                view_count_sum=Coalesce(
                    Sum("articles__view_count", filter=published_filter),
                    0,
                ),
            )
            if not self.request.user.is_staff:
                qs = qs.filter(published_count__gt=0)
            if self.action == "list":
                qs = qs.order_by("-view_count_sum", "-published_count", "name")
        return qs

    @extend_schema(
        summary="Liste des tags",
        description="Récupère la liste des tags d'articles.",
        responses={200: TagSerializer(many=True)},
        tags=["Articles - Tags"],
    )
    def list(self, request, *args, **kwargs):
        """Récupère la liste des tags d'articles."""
        # Pas de cache_page: la reponse varie par is_staff (admin voit les vides)
        # et doit refleter immediatement chaque publication d'article.
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Détails d'un tag",
        description="Récupère les détails d'un tag par son nom.",
        responses={200: TagSerializer, 404: OpenApiResponse(description="Tag non trouve")},
        tags=["Articles - Tags"],
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Récupère les détails d'un tag par son nom."""
        name = str(kwargs.get("name", ""))
        instance = TagService.get_by_name(name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
