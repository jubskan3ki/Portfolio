"""Filtres django-filter pour le module transfer."""

import django_filters

from .models import ExportJob, ImportJob


class ExportJobFilter(django_filters.FilterSet):
    """Filtre pour les jobs d'export."""

    status = django_filters.ChoiceFilter(choices=ExportJob.Status.choices)
    module = django_filters.CharFilter(lookup_expr="iexact")
    format = django_filters.ChoiceFilter(choices=ExportJob.Format.choices)

    # Filtres par date
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    # Tri
    ordering = django_filters.OrderingFilter(
        fields=(
            ("created_at", "date"),
            ("status", "status"),
            ("module", "module"),
        ),
    )

    class Meta:
        model = ExportJob
        fields = ["status", "module", "format"]


class ImportJobFilter(django_filters.FilterSet):
    """Filtre pour les jobs d'import."""

    status = django_filters.ChoiceFilter(choices=ImportJob.Status.choices)
    module = django_filters.CharFilter(lookup_expr="iexact")

    # Filtres par date
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    # Tri
    ordering = django_filters.OrderingFilter(
        fields=(
            ("created_at", "date"),
            ("status", "status"),
            ("module", "module"),
        ),
    )

    class Meta:
        model = ImportJob
        fields = ["status", "module"]
