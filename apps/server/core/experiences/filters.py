"""Filtres django-filter pour le module experiences."""

import django_filters
from django.db.models import QuerySet

from utils.filters import SearchFilterMixin

from .models import Experience, ExperienceType


class ExperienceFilter(SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les experiences."""

    search_fields = ["title", "company", "description"]

    type = django_filters.CharFilter(method="filter_by_type")
    type_id = django_filters.NumberFilter(field_name="type__id")

    # Recherche
    search = django_filters.CharFilter(method="filter_search")
    company = django_filters.CharFilter(lookup_expr="icontains")

    # Filtres par date
    start_after = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="gte",
    )
    start_before = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="lte",
    )

    # Experience en cours
    is_current = django_filters.BooleanFilter(method="filter_is_current")

    # Tri
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


class ExperienceTypeFilter(django_filters.FilterSet):
    """Filtre pour les types d'experiences."""

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ExperienceType
        fields = ["name"]
