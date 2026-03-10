"""Service pour gerer les FAQs."""

from django.db.models import QuerySet

from utils.services import BaseService

from ..models import FAQ


class FAQService(BaseService["FAQ"]):
    """Service pour les operations sur les FAQs."""

    model = FAQ
    entity_name = "FAQ"
    logger_name = "core.contact"

    @classmethod
    def get_all(cls, *, published_only: bool = True) -> QuerySet[FAQ]:
        """Recupere toutes les FAQs."""
        queryset = cls.model.objects.all()
        if published_only:
            queryset = queryset.filter(is_published=True)
        return queryset
