"""Service pour gerer les tags d'articles."""

from django.core.exceptions import ObjectDoesNotExist

from utils.exceptions.service import NotFoundError
from utils.services import BaseService

from ..models import Tag


class TagService(BaseService["Tag"]):
    """Service pour les operations sur les tags d'articles."""

    model = Tag
    entity_name = "Tag"
    logger_name = "core.articles"

    @classmethod
    def get_by_name(cls, name: str) -> Tag:
        """Recupere un tag d'article par son nom."""
        try:
            return cls.model.objects.get(name__iexact=name)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning("Tag non trouve: name=%s", name)
            raise NotFoundError(f"Tag '{name}' non trouve.", details={"name": name}) from exc

    @classmethod
    def get_or_create(cls, name: str) -> tuple[Tag, bool]:
        """Recupere un tag existant ou en cree un nouveau."""
        return Tag.objects.get_or_create(name=name)
