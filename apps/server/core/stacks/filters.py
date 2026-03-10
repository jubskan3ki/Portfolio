"""Filtres django-filter pour le module stacks."""

import django_filters
from django.db.models import QuerySet

from utils.filters import CategoryFilterMixin, SearchFilterMixin

from .models import Stack, StackCategory


class StackFilter(CategoryFilterMixin, SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les stacks."""

    search_fields = ["name", "description"]
    category_lookup_include_slug = False

    # Filtres par categorie
    category = django_filters.CharFilter(method="filter_by_category")
    category_id = django_filters.NumberFilter(field_name="category__id")

    # Recherche textuelle
    search = django_filters.CharFilter(method="filter_search")
    q = django_filters.CharFilter(method="filter_search")

    # Filtres par niveau
    level = django_filters.NumberFilter()
    level_min = django_filters.NumberFilter(field_name="level", lookup_expr="gte")
    level_max = django_filters.NumberFilter(field_name="level", lookup_expr="lte")

    # Tri
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("level", "level"),
            ("created_at", "created_at"),
        ),
    )

    class Meta:
        model = Stack
        fields = [
            "category",
            "category_id",
            "search",
            "level",
            "level_min",
            "level_max",
        ]


class StackCategoryFilter(django_filters.FilterSet):
    """Filtre pour les categories de stacks."""

    name = django_filters.CharFilter(lookup_expr="icontains")
    has_stacks = django_filters.BooleanFilter(method="filter_has_stacks")

    class Meta:
        model = StackCategory
        fields = ["name"]

    def filter_has_stacks(self, queryset: QuerySet, _name: str, *, value: bool) -> QuerySet:
        """Filtre les categories ayant des stacks."""
        if value:
            return queryset.filter(stacks__isnull=False).distinct()
        return queryset.exclude(stacks__isnull=False)
