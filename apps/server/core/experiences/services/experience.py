"""Service pour gerer les experiences professionnelles."""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from utils.services import BaseService

from ..models import Experience


class ExperienceService(BaseService["Experience"]):
    """Service pour les operations sur les experiences."""

    model = Experience
    entity_name = "Experience"
    logger_name = "core.experiences"

    @classmethod
    def _get_base_queryset(cls) -> QuerySet[Experience]:
        """Retourne le queryset de base avec les relations."""
        return Experience.objects.select_related("type")

    @classmethod
    def get_by_type(cls, type_name: str) -> QuerySet[Experience]:
        """Recupere les experiences d'un type specifique."""
        return cls._get_base_queryset().filter(type__name__iexact=type_name)

    @classmethod
    def get_current(cls) -> Experience | None:
        """Recupere l'experience en cours (sans date de fin)."""
        try:
            return cls._get_base_queryset().filter(end_date__isnull=True).latest("start_date")
        except ObjectDoesNotExist:
            return None
