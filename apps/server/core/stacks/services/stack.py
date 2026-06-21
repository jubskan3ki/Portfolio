"""Service pour les stacks techniques."""

from functools import reduce
from operator import or_
from typing import Any

from django.db.models import Q, QuerySet
from django.db.models.fields import TextField
from django.db.models.functions import Cast

from utils.services import BaseService

from ..models import Stack, StackRelationship
from .category import CategoryService


class StackService(BaseService["Stack"]):
    """Service pour les operations sur les stacks."""

    model = Stack
    entity_name = "Stack"
    logger_name = "core.stacks"

    @classmethod
    def _get_base_queryset(cls) -> QuerySet[Stack]:
        """Retourne le queryset de base avec les relations."""
        return Stack.objects.select_related("category")

    @classmethod
    def _get_detail_queryset(cls) -> QuerySet[Stack]:
        """Retourne le queryset pour les details avec prefetch (source unique : manager)."""
        return Stack.objects.with_detail()

    @classmethod
    def get_by_category(cls, category_name: str) -> QuerySet[Stack]:
        """Recupere les stacks d'une categorie."""
        CategoryService.get_by_name(category_name)
        return cls._get_base_queryset().filter(category__name__iexact=category_name)

    @classmethod
    def get_related(cls, stack: Stack) -> tuple[list[Stack], dict[Any, str]]:
        """Recupere les stacks associees a une stack.

        Retourne les Stack cibles et la map {pk: relationship_type} attendue par
        RelatedStackSerializer (source unique du dict de sortie). NULL-safe :
        category est gere par le serializer (StringRelatedField).
        """
        relationships = StackRelationship.objects.filter(from_stack=stack).select_related(
            "to_stack", "to_stack__category"
        )

        related_stacks: list[Stack] = []
        relationship_map: dict[Any, str] = {}
        for rel in relationships:
            related_stacks.append(rel.to_stack)
            relationship_map[rel.to_stack.pk] = rel.relationship_type

        return related_stacks, relationship_map

    @classmethod
    def get_projects_for_stack(cls, stack: Stack) -> QuerySet:
        """Recupere les projets utilisant cette stack (matching souple par nom + tags)."""
        from core.projects.models import Project

        terms = [stack.name] + (stack.tags if isinstance(stack.tags, list) else [])
        if not terms:
            return Project.objects.none()

        tech_text = Cast("technologies", TextField())
        q_filters = reduce(or_, (Q(tech_text__icontains=term) for term in terms))

        return (
            Project.objects.annotate(tech_text=tech_text)
            .filter(q_filters)
            .select_related("category", "status")
            .distinct()[:3]
        )

    @classmethod
    def get_articles_for_stack(cls, stack: Stack) -> QuerySet:
        """Recupere les articles lies a cette stack (matching par tags)."""
        from core.articles.models import Article

        tag_names = [stack.name] + (stack.tags if isinstance(stack.tags, list) else [])
        if not tag_names:
            return Article.objects.none()

        return (
            Article.objects.filter(is_published=True, tags__name__in=tag_names)
            .select_related("category")
            .prefetch_related("tags")
            .distinct()[:3]
        )
