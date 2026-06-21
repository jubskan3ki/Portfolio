"""Service pour gerer les categories d'articles."""

from django.db.models import QuerySet

from utils.services import BaseService

from ..models import Category


class CategoryService(BaseService["Category"]):
    """Service pour les operations sur les categories d'articles."""

    model = Category
    entity_name = "Categorie d'article"
    logger_name = "core.articles"

    @classmethod
    def _get_detail_queryset(cls) -> QuerySet[Category]:
        """Annote published_count pour que le detail expose le bon compteur.

        Sans annotation, la propriete article_count retombe sur 0 (le detail
        passait par le manager nu via get_by_slug).
        """
        return Category.objects.with_article_count()
