"""Services utilitaires."""

import logging
from typing import Any, ClassVar, Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import F, QuerySet

from utils.exceptions.service import NotFoundError

T = TypeVar("T", bound=models.Model)


def apply_update(
    instance: models.Model,
    data: dict[str, Any],
    *,
    partial: bool = False,
    m2m_fields: dict[str, Any] | None = None,
) -> None:
    """Applique un dict de mises a jour sur une instance de modele.

    En mode partial, les valeurs None sont ignorees.

    Args:
        instance: Instance Django a mettre a jour.
        data: Dictionnaire des champs scalaires a modifier.
        partial: Si True, ignore les valeurs None.
        m2m_fields: Dictionnaire {field_name: iterable_of_values} pour les
            relations ManyToMany. Les valeurs sont passees a set().
    """
    for key, value in data.items():
        if partial and value is None:
            continue
        setattr(instance, key, value)

    if m2m_fields:
        instance.save()
        for field_name, values in m2m_fields.items():
            getattr(instance, field_name).set(values)


class BaseService(Generic[T]):
    """Service de base fournissant les operations CRUD standard.

    Sous-classes doivent definir:
        model: La classe du modele Django.
        entity_name: Nom lisible pour les logs et messages d'erreur.
        logger_name: Nom du logger (ex: "core.projects").

    Methodes a overrider si necessaire:
        _get_base_queryset: Pour ajouter select_related sur les listes.
        _get_detail_queryset: Pour ajouter prefetch_related sur les details.
    """

    model: ClassVar[type[T]]
    entity_name: ClassVar[str]
    logger_name: ClassVar[str]

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        return logging.getLogger(cls.logger_name)

    @classmethod
    def _get_base_queryset(cls) -> QuerySet[T]:
        """Queryset pour les listes (select_related)."""
        return cls.model.objects.all()

    @classmethod
    def _get_detail_queryset(cls) -> QuerySet[T]:
        """Queryset pour les details (select_related + prefetch_related).

        Par defaut, utilise le queryset de base.
        """
        return cls._get_base_queryset()

    @classmethod
    def get_by_id(cls, obj_id: int) -> T:
        """Recupere une instance par son ID.

        Raises:
            NotFoundError: Si l'instance n'existe pas.
        """
        try:
            return cls._get_detail_queryset().get(id=obj_id)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning("%s non trouve: id=%s", cls.entity_name, obj_id)
            raise NotFoundError(
                f"{cls.entity_name} avec l'ID {obj_id} non trouve.",
                details={"id": obj_id},
            ) from exc

    @classmethod
    def get_by_slug(cls, slug: str) -> T:
        """Recupere une instance par son slug.

        Raises:
            NotFoundError: Si l'instance n'existe pas.
        """
        try:
            return cls._get_detail_queryset().get(slug=slug)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning("%s non trouve: slug=%s", cls.entity_name, slug)
            raise NotFoundError(
                f"{cls.entity_name} avec le slug '{slug}' non trouve.",
                details={"slug": slug},
            ) from exc

    @classmethod
    @transaction.atomic
    def create(cls, data: dict[str, Any]) -> T:
        """Cree une nouvelle instance.

        Args:
            data: Donnees validees.

        Returns:
            L'instance creee.
        """
        instance = cls.model.objects.create(**data)
        cls._get_logger().info("%s cree: id=%s", cls.entity_name, instance.pk)
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, obj_id: int, data: dict[str, Any], *, partial: bool = False) -> T:
        """Met a jour une instance existante.

        Args:
            obj_id: ID de l'instance.
            data: Donnees a mettre a jour.
            partial: Si True, les valeurs None sont ignorees.

        Returns:
            L'instance mise a jour.

        Raises:
            NotFoundError: Si l'instance n'existe pas.
        """
        instance = cls.get_by_id(obj_id)
        apply_update(instance, data, partial=partial)
        instance.save()
        cls._get_logger().info("%s mis a jour: id=%s", cls.entity_name, obj_id)
        return instance

    @classmethod
    def delete(cls, obj_id: int) -> None:
        """Supprime une instance.

        Args:
            obj_id: ID de l'instance.

        Raises:
            NotFoundError: Si l'instance n'existe pas.
        """
        instance = cls.get_by_id(obj_id)
        instance.delete()
        cls._get_logger().info("%s supprime: id=%s", cls.entity_name, obj_id)

    @classmethod
    def exists(cls, slug: str) -> bool:
        """Verifie si une instance avec ce slug existe."""
        return cls.model.objects.filter(slug=slug).exists()


def increment_view_count(instance: models.Model, field_name: str = "view_count") -> None:
    """Incremente atomiquement un compteur de vues sur une instance.

    Utilise une requete UPDATE directe avec F() pour eviter les race conditions.

    Args:
        instance: Instance Django avec un champ compteur.
        field_name: Nom du champ a incrementer.
    """
    model_class: type[models.Model] = instance.__class__
    model_class.objects.filter(pk=instance.pk).update(**{field_name: F(field_name) + 1})


__all__ = ["BaseService", "apply_update", "increment_view_count"]
