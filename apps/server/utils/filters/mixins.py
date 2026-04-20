"""Mixins de filtrage reutilisables pour django-filter."""

from typing import ClassVar

from django.db.models import Q, QuerySet


class CategoryFilterMixin:
    """Filtre par slug ou nom (iexact). category_lookup_include_slug=False: nom uniquement."""

    category_lookup_include_slug: ClassVar[bool] = True

    def filter_by_category(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        if self.category_lookup_include_slug:
            return queryset.filter(Q(category__slug=value) | Q(category__name__iexact=value))
        return queryset.filter(category__name__iexact=value)


class SearchFilterMixin:
    """Recherche icontains sur search_fields (defini par sous-classe)."""

    search_fields: ClassVar[list[str]] = []

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        if not self.search_fields:
            return queryset
        q = Q()
        for field in self.search_fields:
            q |= Q(**{f"{field}__icontains": value})
        return queryset.filter(q)
