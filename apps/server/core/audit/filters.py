"""Filtres django-filter pour le module audit."""

import django_filters
from django.db.models import Q, QuerySet

from .models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    """Filtre pour les logs d'audit."""

    action = django_filters.ChoiceFilter(choices=AuditLog.Action.choices)
    model_name = django_filters.CharFilter(lookup_expr="iexact")
    object_id = django_filters.CharFilter()
    user = django_filters.NumberFilter(field_name="user__id")

    date_after = django_filters.DateTimeFilter(
        field_name="timestamp",
        lookup_expr="gte",
    )
    date_before = django_filters.DateTimeFilter(
        field_name="timestamp",
        lookup_expr="lte",
    )

    search = django_filters.CharFilter(method="filter_search")

    ordering = django_filters.OrderingFilter(
        fields=(
            ("timestamp", "date"),
            ("action", "action"),
            ("model_name", "model"),
        ),
    )

    class Meta:
        model = AuditLog
        fields = [
            "action",
            "model_name",
            "object_id",
            "user",
            "date_after",
            "date_before",
        ]

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Recherche dans object_repr et correlation_id."""
        return queryset.filter(Q(object_repr__icontains=value) | Q(correlation_id__icontains=value))
