"""Filtres django-filter pour le module experiences."""

import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, QuerySet

from utils.filters import SearchFilterMixin

from .models import Experience, ExperienceType

SEARCH_CONFIG = "french_unaccent"


class ExperienceFilter(SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les experiences."""

    search_fields = ["title", "company", "description"]

    type = django_filters.CharFilter(method="filter_by_type")
    type_id = django_filters.NumberFilter(field_name="type__id")

    search = django_filters.CharFilter(method="filter_search")
    q = django_filters.CharFilter(method="filter_search")
    company = django_filters.CharFilter(lookup_expr="icontains")

    start_after = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="gte",
    )
    start_before = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="lte",
    )

    is_current = django_filters.BooleanFilter(method="filter_is_current")

    ordering = django_filters.OrderingFilter(
        fields=(
            ("start_date", "date"),
            ("start_date", "start_date"),
            ("company", "company"),
            ("title", "title"),
        ),
    )

    class Meta:
        model = Experience
        fields = [
            "type",
            "type_id",
            "company",
            "is_current",
            "start_after",
            "start_before",
        ]

    def filter_by_type(
        self,
        queryset: QuerySet,
        _name: str,
        value: str,
    ) -> QuerySet:
        """Filtre par nom de type d'experience."""
        return queryset.filter(type__name__iexact=value)

    def filter_is_current(
        self,
        queryset: QuerySet,
        _name: str,
        value: bool,  # noqa: FBT001
    ) -> QuerySet:
        """Filtre les experiences en cours."""
        if value:
            return queryset.filter(end_date__isnull=True)
        return queryset.filter(end_date__isnull=False)

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Recherche Full-Text PostgreSQL via search_vector (fallback icontains hors PG)."""
        if not value or len(value.strip()) < 2:
            return queryset
        if "postgresql" not in self._get_db_engine(queryset.db):
            return super().filter_search(queryset, _name, value)
        search_query = SearchQuery(value, config=SEARCH_CONFIG, search_type="websearch")
        return (
            queryset.annotate(rank=SearchRank(F("search_vector"), search_query))
            .filter(search_vector=search_query)
            .order_by("-rank")
        )

    @staticmethod
    def _get_db_engine(db_alias: str) -> str:
        from django.conf import settings

        return settings.DATABASES.get(db_alias, {}).get("ENGINE", "")


class ExperienceTypeFilter(django_filters.FilterSet):
    """Filtre pour les types d'experiences."""

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ExperienceType
        fields = ["name"]
