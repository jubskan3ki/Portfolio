"""Vues pour les catégories d'articles."""

from typing import Any

from django.db.models import QuerySet
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
    # Liste complete renvoyee sans pagination (consommee en sidebar/admin-select).
    pagination_class = None

    serializer_classes = {
        "list": CategorySerializer,
        "detail": CategorySerializer,
        "write": CategorySerializer,
    }

    def get_queryset(self) -> QuerySet[Category]:
        """Filtre + ordonne les catégories selon l'action.

        - list/retrieve: annote published_count.
        - Public: exclut les catégories sans article publié (published_count > 0).
        - list: tri par published_count DESC, puis name.
        """
        qs = super().get_queryset()
        if self.action in ("list", "retrieve"):
            qs = qs.with_article_count()
            if not self.request.user.is_staff:
                qs = qs.filter(published_count__gt=0)
            if self.action == "list":
                qs = qs.order_by("-published_count", "name")
        return qs

    @extend_schema(
        summary="Liste des catégories",
        description="Récupère la liste des catégories d'articles.",
        responses={200: CategorySerializer(many=True)},
        tags=["Articles - Catégories"],
    )
    def list(self, request, *args, **kwargs):
        """Récupère la liste des catégories d'articles."""
        # Pas de cache_page : la reponse varie par is_staff et doit refleter immediatement chaque publication.
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Détails d'une catégorie",
        description="Récupère les détails d'une catégorie par son slug.",
        responses={200: CategorySerializer, 404: OpenApiResponse(description="Categorie non trouvee")},
        tags=["Articles - Catégories"],
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Récupère les détails d'une catégorie par son slug."""
        slug = str(kwargs.get("slug", ""))
        instance = CategoryService.get_by_slug(slug)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
