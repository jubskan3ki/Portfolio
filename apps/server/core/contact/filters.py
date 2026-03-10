"""Filtres django-filter pour le module contact."""

import django_filters
from django.db.models import Q, QuerySet

from .models import FAQ, Contact


class ContactFilter(django_filters.FilterSet):
    """Filtre pour les soumissions de contact."""

    status = django_filters.ChoiceFilter(choices=Contact.STATUS_CHOICES)
    email = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    # Recherche
    search = django_filters.CharFilter(method="filter_search")

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
            ("name", "name"),
        ),
    )

    class Meta:
        model = Contact
        fields = [
            "status",
            "email",
            "name",
            "created_after",
            "created_before",
        ]

    def filter_search(
        self,
        queryset: QuerySet,
        _name: str,
        value: str,
    ) -> QuerySet:
        """Recherche dans nom, email, sujet et message."""
        return queryset.filter(
            Q(name__icontains=value)
            | Q(email__icontains=value)
            | Q(subject__icontains=value)
            | Q(message__icontains=value)
        )


class FAQFilter(django_filters.FilterSet):
    """Filtre pour les FAQs."""

    is_published = django_filters.BooleanFilter()
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = FAQ
        fields = ["is_published"]

    def filter_search(
        self,
        queryset: QuerySet,
        _name: str,
        value: str,
    ) -> QuerySet:
        """Recherche dans question et reponse."""
        return queryset.filter(Q(question__icontains=value) | Q(answer__icontains=value))
