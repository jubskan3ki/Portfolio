"""
Vues pour les catégories d'articles avec CRUD complet.
"""

from typing import Any

from django.db.models import Count, Q, QuerySet
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..models import Category
from ..serializers.category import CategorySerializer
from ..services.category import CategoryService
from ..throttles import ArticlesThrottle


class CategoryViewSet(BaseAPIViewSet):
    """
    API endpoint pour les catégories d'articles.

    Hérite de BaseAPIViewSet :
    - Permissions admin pour écriture (AdminWritePermissionMixin)
    - Logging automatique des actions CRUD (LoggingMixin)
    - Lookup par slug ou pk (SlugOrPkLookupMixin)
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [ArticlesThrottle]
    lookup_field = "slug"

    serializer_classes = {
        "list": CategorySerializer,
        "detail": CategorySerializer,
        "write": CategorySerializer,
    }

    def get_queryset(self) -> QuerySet[Category]:
        """Filtre les catégories pour n'afficher que celles ayant des articles publiés (public)."""
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
        summary="Liste des catégories",
        description="Récupère la liste des catégories d'articles.",
        responses={200: CategorySerializer(many=True)},
        tags=["Articles - Catégories"],
    )
    @method_decorator(cache_page(1800))
    def list(self, request, *args, **kwargs):
        """Récupère la liste des catégories d'articles."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Détails d'une catégorie",
        description="Récupère les détails d'une catégorie par son slug.",
        responses={200: CategorySerializer, 404: OpenApiResponse(description="Categorie non trouvee")},
        tags=["Articles - Catégories"],
    )
    @method_decorator(cache_page(1800))
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Récupère les détails d'une catégorie par son slug."""
        slug = str(kwargs.get("slug", ""))
        instance = CategoryService.get_by_slug(slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
