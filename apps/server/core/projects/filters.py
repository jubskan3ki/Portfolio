"""Filtres django-filter pour le module projects."""

import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, QuerySet

from utils.filters import CategoryFilterMixin, SearchFilterMixin, build_prefix_tsquery

from .models import Project, ProjectCategory, ProjectStatus

SEARCH_CONFIG = "french_unaccent"


class ProjectFilter(CategoryFilterMixin, SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les projets."""

    search_fields = ["title", "description", "long_description"]

    category = django_filters.CharFilter(method="filter_by_category")
    category_id = django_filters.NumberFilter(field_name="category__id")

    status = django_filters.CharFilter(method="filter_by_status")
    status_id = django_filters.NumberFilter(field_name="status__id")

    technologies = django_filters.CharFilter(method="filter_by_technologies")

    search = django_filters.CharFilter(method="filter_search")
    q = django_filters.CharFilter(method="filter_search")

    date_after = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
    )
    date_before = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
    )

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
            "technologies",
            "search",
            "date_after",
            "date_before",
        ]

    def filter_by_status(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Filtre par nom de statut."""
        return queryset.filter(status__name__iexact=value)

    def filter_by_technologies(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Filtre par technologies (liste JSON, AND entre les valeurs separees par virgule).

        Utilise le lookup `__contains` de JSONField : chaque technologie demandee doit etre
        presente dans le tableau. Frontend envoie `?technologies=Vue,TypeScript`.
        """
        techs = [t.strip() for t in value.split(",") if t.strip()]
        if not techs:
            return queryset
        filtered = queryset
        for tech in techs:
            filtered = filtered.filter(technologies__contains=[tech])
        return filtered

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Recherche Full-Text PostgreSQL avec prefix matching (fallback icontains hors PG).

        Utilise `tsquery` en mode raw pour activer l'operateur `:*` (ex: `nux:*` matche
        Nuxt). Permet aux utilisateurs de trouver un resultat meme avec une saisie
        partielle.
        """
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
