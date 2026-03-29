"""Service pour les projets."""

from django.db.models import QuerySet

from config.constants import DEFAULT_FEATURED_PROJECTS
from utils.cache.decorators import cached_queryset
from utils.cache.keys import CacheKeys
from utils.services import BaseService

from ..models import Project, ProjectCategory


class ProjectService(BaseService["Project"]):
    """Service pour les operations sur les projets.

    Herite de BaseService: get_by_id, get_by_slug, create, update, delete, exists.
    """

    model = Project
    entity_name = "Projet"
    logger_name = "core.projects"

    @classmethod
    def _get_base_queryset(cls) -> QuerySet[Project]:
        """Retourne le queryset de base avec les relations."""
        return Project.objects.select_related("category", "status")

    @classmethod
    @cached_queryset(
        CacheKeys.project_list,
        timeout=CacheKeys.TTL_MEDIUM,
    )
    def get_by_category(cls, category_slug: str) -> QuerySet[Project]:
        """Recupere les projets d'une categorie."""
        try:
            category = ProjectCategory.objects.get(slug=category_slug)
        except ProjectCategory.DoesNotExist:
            cls._get_logger().warning("Categorie non trouvee: slug=%s", category_slug)
            return Project.objects.none()
        return cls._get_base_queryset().filter(category=category)

    @classmethod
    @cached_queryset(
        lambda limit=DEFAULT_FEATURED_PROJECTS: CacheKeys.project_featured(limit),
        timeout=CacheKeys.TTL_MEDIUM,
    )
    def get_featured(cls, limit: int = DEFAULT_FEATURED_PROJECTS) -> QuerySet[Project]:
        """Recupere les projets mis en avant (les plus vus)."""
        return cls._get_base_queryset().order_by("-view_count")[:limit]
