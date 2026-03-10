"""Service pour les categories de stacks."""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, QuerySet

from utils.exceptions.service import NotFoundError
from utils.services import BaseService

from ..models import StackCategory


class CategoryService(BaseService["StackCategory"]):
    """Service pour les operations sur les categories."""

    model = StackCategory
    entity_name = "Categorie de stack"
    logger_name = "core.stacks"

    VALID_SORT_FIELDS = ("name", "stacks_count")

    @classmethod
    def get_all(
        cls,
        *,
        with_count: bool = True,
        order_by: str = "name",
    ) -> QuerySet[StackCategory]:
        """Recupere toutes les categories.

        Args:
            with_count: Ajoute le comptage des stacks.
            order_by: Champ de tri.

        Returns:
            QuerySet des categories.
        """
        queryset = cls.model.objects.all()

        if with_count:
            queryset = queryset.annotate(stacks_count=Count("stacks"))

        if order_by in cls.VALID_SORT_FIELDS:
            queryset = queryset.order_by(order_by)

        return queryset

    @classmethod
    def get_by_name(cls, name: str) -> StackCategory:
        """Recupere une categorie par nom.

        Args:
            name: Nom de la categorie.

        Returns:
            La categorie trouvee.

        Raises:
            NotFoundError: Si la categorie n'existe pas.
        """
        try:
            return cls.model.objects.get(name__iexact=name)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning("Categorie non trouvee: name=%s", name)
            raise NotFoundError(
                f"Categorie '{name}' non trouvee.",
                details={"name": name},
            ) from exc

    @classmethod
    def exists(cls, name: str) -> bool:
        """Verifie si une categorie existe."""
        return cls.model.objects.filter(name__iexact=name).exists()
