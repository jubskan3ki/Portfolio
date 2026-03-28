"""Views pour les ressources de stacks."""

from typing import Any, cast

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet

from ..doc import RESOURCE_LIST_PARAMS, RESPONSE_204, RESPONSE_400, RESPONSE_404, TAGS_RESOURCES
from ..models import StackResource
from ..serializers import StackResourceSerializer
from ..services.resource import ResourceService
from ..throttles import StacksThrottle


class ResourceViewSet(BaseAPIViewSet):
    """API endpoint pour les ressources de stacks."""

    queryset = StackResource.objects.all()
    serializer_class = StackResourceSerializer
    throttle_classes = (StacksThrottle,)

    def _get_base_queryset(self):
        """Retourne les ressources filtrees."""
        filters = self._extract_filters()
        return ResourceService.get_all(filters)

    def _extract_filters(self) -> dict[str, Any]:
        """Extrait les filtres des query params."""
        params = cast(Request, self.request).query_params
        filters: dict[str, Any] = {}

        if stack_id := params.get("stack_id"):
            filters["stack_id"] = stack_id
        if stack_slug := params.get("stack_slug"):
            filters["stack_slug"] = stack_slug
        if resource_type := params.get("type"):
            filters["type"] = resource_type

        return filters

    @extend_schema(
        summary="Liste des ressources",
        description="Recupere les ressources avec filtres optionnels.",
        parameters=RESOURCE_LIST_PARAMS,
        responses={200: StackResourceSerializer(many=True)},
        tags=TAGS_RESOURCES,
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Liste des ressources."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Details d'une ressource",
        description="Recupere une ressource par son ID.",
        responses={200: StackResourceSerializer, 404: RESPONSE_404},
        tags=TAGS_RESOURCES,
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Details d'une ressource."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Creer une ressource",
        description="Cree une nouvelle ressource.",
        request=StackResourceSerializer,
        responses={201: StackResourceSerializer, 400: RESPONSE_400},
        tags=TAGS_RESOURCES,
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Cree une ressource."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier une ressource",
        description="Met a jour completement une ressource.",
        request=StackResourceSerializer,
        responses={200: StackResourceSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_RESOURCES,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une ressource."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier partiellement une ressource",
        description="Met a jour partiellement une ressource.",
        request=StackResourceSerializer,
        responses={200: StackResourceSerializer, 400: RESPONSE_400, 404: RESPONSE_404},
        tags=TAGS_RESOURCES,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une ressource."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer une ressource",
        description="Supprime une ressource existante.",
        responses={204: RESPONSE_204, 404: RESPONSE_404},
        tags=TAGS_RESOURCES,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une ressource."""
        return super().destroy(request, *args, **kwargs)
