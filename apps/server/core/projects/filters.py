"""Filtres django-filter pour le module projects."""

import django_filters
from django.db.models import QuerySet

from utils.filters import CategoryFilterMixin, SearchFilterMixin

from .models import Project, ProjectCategory, ProjectStatus


class ProjectFilter(CategoryFilterMixin, SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les projets."""

    search_fields = ["title", "description"]

    # Filtres par categorie
    category = django_filters.CharFilter(method="filter_by_category")
    category_id = django_filters.NumberFilter(field_name="category__id")

    # Filtres par statut
    status = django_filters.CharFilter(method="filter_by_status")
    status_id = django_filters.NumberFilter(field_name="status__id")

    # Recherche textuelle
    search = django_filters.CharFilter(method="filter_search")
    q = django_filters.CharFilter(method="filter_search")

    # Filtres par date
    date_after = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
    )
    date_before = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
    )

    # Tri
    ordering = django_filters.OrderingFilter(
        fields=(
            ("date", "date"),
            ("title", "title"),
            ("view_count", "views"),
            ("created_at", "created_at"),
        ),
    )

    class Meta:
        model = Project
        fields = [
            "category",
            "category_id",
            "status",
            "status_id",
            "search",
            "date_after",
            "date_before",
        ]

    def filter_by_status(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Filtre par nom de statut."""
        return queryset.filter(status__name__iexact=value)


class ProjectCategoryFilter(django_filters.FilterSet):
    """Filtre pour les categories de projets."""

    name = django_filters.CharFilter(lookup_expr="icontains")
    has_projects = django_filters.BooleanFilter(method="filter_has_projects")

    class Meta:
        model = ProjectCategory
        fields = ["name", "slug"]

    def filter_has_projects(self, queryset: QuerySet, _name: str, *, value: bool) -> QuerySet:
        """Filtre les categories ayant des projets."""
        if value:
            return queryset.filter(projects__isnull=False).distinct()
        return queryset.exclude(projects__isnull=False)


class ProjectStatusFilter(django_filters.FilterSet):
    """Filtre pour les statuts de projets."""

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ProjectStatus
        fields = ["name"]
