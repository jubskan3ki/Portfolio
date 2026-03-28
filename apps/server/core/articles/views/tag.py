"""
Vues pour les tags d'articles avec CRUD complet.
"""

from django.db.models import Count, Q, QuerySet
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import OpenApiResponse, extend_schema
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

    serializer_classes = {
        "list": TagSerializer,
        "detail": TagSerializer,
        "write": TagSerializer,
    }

    def get_queryset(self) -> QuerySet[Tag]:
        """Filtre les tags pour n'afficher que ceux ayant des articles publiés (public)."""
        qs = super().get_queryset()
        if self.action in ("list", "retrieve"):
            now = timezone.now()
            qs = qs.annotate(
                published_count=Count(
                    "articles",
                    filter=Q(articles__is_published=True, articles__published_date__lte=now),
                )
            )
            if not self.request.user.is_staff:
                qs = qs.filter(published_count__gt=0)
        return qs

    @extend_schema(
        summary="Liste des tags",
        description="Récupère la liste des tags d'articles.",
        responses={200: TagSerializer(many=True)},
        tags=["Articles - Tags"],
    )
    @method_decorator(cache_page(1800))
    def list(self, request, *args, **kwargs):
        """Récupère la liste des tags d'articles."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Détails d'un tag",
        description="Récupère les détails d'un tag par son nom.",
        responses={200: TagSerializer, 404: OpenApiResponse(description="Tag non trouve")},
        tags=["Articles - Tags"],
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, _request, *_args, **kwargs):
        """Récupère les détails d'un tag par son nom."""
        name = str(kwargs.get("name", ""))
        instance = TagService.get_by_name(name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
