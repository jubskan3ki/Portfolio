"""Mixins de filtrage reutilisables pour django-filter."""

from typing import ClassVar

from django.db.models import Q, QuerySet


class CategoryFilterMixin:
    """Mixin pour filtrer par categorie (slug ou nom).

    Fournit ``filter_by_category`` qui cherche par slug OU nom (case-insensitive).
    Si ``category_lookup_include_slug`` est False, seul le nom est utilise.
    """

    category_lookup_include_slug: ClassVar[bool] = True

    def filter_by_category(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Filtre par nom ou slug de categorie."""
        if self.category_lookup_include_slug:
            return queryset.filter(Q(category__slug=value) | Q(category__name__iexact=value))
        return queryset.filter(category__name__iexact=value)


class SearchFilterMixin:
    """Mixin pour la recherche textuelle multi-champs.

    Sous-classes doivent definir ``search_fields`` avec les noms de champs
    a rechercher (lookup ``icontains``).
    """

    search_fields: ClassVar[list[str]] = []

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Recherche textuelle dans les champs definis."""
        if not self.search_fields:
            return queryset
        q = Q()
        for field in self.search_fields:
            q |= Q(**{f"{field}__icontains": value})
        return queryset.filter(q)
