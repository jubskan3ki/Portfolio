"""Filtres django-filter pour le module stacks."""

import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, QuerySet

from utils.filters import CategoryFilterMixin, SearchFilterMixin, build_prefix_tsquery

from .models import Stack, StackCategory

SEARCH_CONFIG = "french_unaccent"


class StackFilter(CategoryFilterMixin, SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les stacks."""

    search_fields = ["name", "description", "content"]
    category_lookup_include_slug = False

    category = django_filters.CharFilter(method="filter_by_category")
    category_id = django_filters.NumberFilter(field_name="category__id")

    search = django_filters.CharFilter(method="filter_search")
    q = django_filters.CharFilter(method="filter_search")

    level = django_filters.NumberFilter()
    level_min = django_filters.NumberFilter(field_name="level", lookup_expr="gte")
    level_max = django_filters.NumberFilter(field_name="level", lookup_expr="lte")

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

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Recherche Full-Text PostgreSQL avec prefix matching (fallback hors PG)."""
        if not value or len(value.strip()) < 2:
            return queryset
        if "postgresql" not in self._get_db_engine(queryset.db):
            return super().filter_search(queryset, _name, value)
        raw_tsquery = build_prefix_tsquery(value)
        if not raw_tsquery:
            return queryset
        search_query = SearchQuery(raw_tsquery, config=SEARCH_CONFIG, search_type="raw")
        return (
            queryset.annotate(rank=SearchRank(F("search_vector"), search_query))
            .filter(search_vector=search_query)
            .order_by("-rank")
        )

    @staticmethod
    def _get_db_engine(db_alias: str) -> str:
        from django.conf import settings

        return settings.DATABASES.get(db_alias, {}).get("ENGINE", "")


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
