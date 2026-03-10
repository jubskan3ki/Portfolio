"""Service pour les categories de projets."""

from django.db.models import Count, QuerySet

from utils.services import BaseService

from ..models import ProjectCategory


class CategoryService(BaseService["ProjectCategory"]):
    """Service pour les operations sur les categories de projets."""

    model = ProjectCategory
    entity_name = "Categorie de projet"
    logger_name = "core.projects"

    @classmethod
    def get_all(cls, *, with_count: bool = False) -> QuerySet[ProjectCategory]:
        """Recupere toutes les categories.

        Args:
            with_count: Ajoute le comptage des projets.

        Returns:
            QuerySet des categories.
        """
        queryset = cls.model.objects.all().order_by("name")

        if with_count:
            queryset = queryset.annotate(projects_count=Count("projects"))

        return queryset

    @classmethod
    def exists(cls, slug: str) -> bool:
        """Verifie si une categorie existe."""
        return cls.model.objects.filter(slug=slug).exists()
