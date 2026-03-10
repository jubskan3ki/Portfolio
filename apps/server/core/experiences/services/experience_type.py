"""Service pour gerer les types d'experiences."""

from django.core.exceptions import ObjectDoesNotExist

from utils.exceptions.service import NotFoundError
from utils.services import BaseService

from ..models import ExperienceType


class ExperienceTypeService(BaseService["ExperienceType"]):
    """Service pour les operations sur les types d'experiences."""

    model = ExperienceType
    entity_name = "Type d'experience"
    logger_name = "core.experiences"

    @classmethod
    def get_by_name(cls, name: str) -> ExperienceType:
        """Recupere un type d'experience par son nom.

        Args:
            name: Nom du type.

        Returns:
            Le type trouve.

        Raises:
            NotFoundError: Si le type n'existe pas.
        """
        try:
            return cls.model.objects.get(name__iexact=name)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning("Type d'experience non trouve: name=%s", name)
            raise NotFoundError(
                f"Type d'experience '{name}' non trouve.",
                details={"name": name},
            ) from exc
