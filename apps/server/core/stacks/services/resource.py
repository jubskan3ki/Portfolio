"""Service pour les ressources de stacks."""

import logging
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from config.constants import DEFAULT_FEATURED_RESOURCES
from utils.exceptions.service import NotFoundError

from ..models import RESOURCE_TYPES, StackResource

logger = logging.getLogger("core.stacks")

VALID_RESOURCE_TYPES = [rt[0] for rt in RESOURCE_TYPES]


class ResourceService:
    """Service pour les operations sur les ressources."""

    @staticmethod
    def get_all(filters: dict[str, Any] | None = None) -> QuerySet[StackResource]:
        """Recupere les ressources avec filtres optionnels.

        Args:
            filters: Dictionnaire de filtres (stack_id, stack_slug, type).

        Returns:
            QuerySet des ressources.
        """
        queryset = StackResource.objects.select_related("stack", "stack__category")

        if not filters:
            return queryset

        if stack_id := filters.get("stack_id"):
            queryset = queryset.filter(stack_id=stack_id)
        elif stack_slug := filters.get("stack_slug"):
            queryset = queryset.filter(stack__slug=stack_slug)

        if resource_type := filters.get("type"):
            if resource_type in VALID_RESOURCE_TYPES:
                queryset = queryset.filter(type=resource_type)
            else:
                logger.warning("Type de ressource invalide: %s", resource_type)

        return queryset

    @staticmethod
    def get_by_id(resource_id: int) -> StackResource:
        """Recupere une ressource par ID.

        Args:
            resource_id: ID de la ressource.

        Returns:
            La ressource trouvee.

        Raises:
            NotFoundError: Si la ressource n'existe pas.
        """
        try:
            return StackResource.objects.select_related("stack").get(id=resource_id)
        except ObjectDoesNotExist as exc:
            logger.warning("Ressource non trouvee: id=%s", resource_id)
            raise NotFoundError(
                f"Ressource avec l'ID {resource_id} non trouvee.",
                details={"id": resource_id},
            ) from exc

    @staticmethod
    def get_by_stack(stack_id: int) -> QuerySet[StackResource]:
        """Recupere les ressources d'une stack."""
        return StackResource.objects.filter(stack_id=stack_id).order_by("-is_featured", "title")

    @staticmethod
    def get_by_stack_slug(stack_slug: str) -> QuerySet[StackResource]:
        """Recupere les ressources d'une stack par son slug."""
        return StackResource.objects.filter(stack__slug=stack_slug).order_by("-is_featured", "title")

    @staticmethod
    def get_featured(limit: int = DEFAULT_FEATURED_RESOURCES) -> QuerySet[StackResource]:
        """Recupere les ressources mises en avant."""
        return StackResource.objects.filter(is_featured=True).select_related("stack")[:limit]
