"""Service pour gerer les categories d'articles."""

from utils.services import BaseService

from ..models import Category


class CategoryService(BaseService["Category"]):
    """Service pour les operations sur les categories d'articles."""

    model = Category
    entity_name = "Categorie d'article"
    logger_name = "core.articles"
