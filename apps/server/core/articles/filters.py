"""Filtres django-filter pour le module articles."""

import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import QuerySet

from utils.filters import CategoryFilterMixin, SearchFilterMixin

from .models import Article, Category, Tag


class ArticleFilter(CategoryFilterMixin, SearchFilterMixin, django_filters.FilterSet):
    """Filtre pour les articles.

    Surcharge filter_search pour utiliser la recherche Full-Text PostgreSQL
    avec ranking par pertinence (titre > extrait > contenu).
    """

    search_fields = ["title", "content", "excerpt"]

    # Filtres par categorie
    category = django_filters.CharFilter(method="filter_by_category")
    category_id = django_filters.NumberFilter(field_name="category__id")

    # Filtres par tag
    tag = django_filters.CharFilter(method="filter_by_tag")
    tags = django_filters.CharFilter(method="filter_by_tags")

    # Recherche textuelle
    search = django_filters.CharFilter(method="filter_search")

    # Filtres par date
    published_after = django_filters.DateFilter(
        field_name="published_date",
        lookup_expr="gte",
    )
    published_before = django_filters.DateFilter(
        field_name="published_date",
        lookup_expr="lte",
    )

    # Filtres booleen
    is_published = django_filters.BooleanFilter()
    is_featured = django_filters.BooleanFilter()

    # Tri
    ordering = django_filters.OrderingFilter(
        fields=(
            ("published_date", "date"),
            ("view_count", "views"),
            ("read_time", "readTime"),
            ("title", "title"),
            ("created_at", "created_at"),
        ),
    )

    class Meta:
        model = Article
        fields = [
            "category",
            "category_id",
            "tag",
            "tags",
            "search",
            "is_published",
            "is_featured",
            "published_after",
            "published_before",
        ]

    def filter_search(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Recherche Full-Text PostgreSQL avec ranking par pertinence.

        Surcharge le mixin SearchFilterMixin pour utiliser SearchVector/SearchRank
        au lieu de icontains. Preserve le queryset filtre existant.
        """
        if not value or len(value.strip()) < 2:
            return queryset
        search_vector = (
            SearchVector("title", weight="A", config="french")
            + SearchVector("excerpt", weight="B", config="french")
            + SearchVector("content", weight="C", config="french")
        )
        search_query = SearchQuery(value, config="french")
        return queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.01).order_by("-rank")

    def filter_by_tag(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Filtre par nom de tag."""
        return queryset.filter(tags__name__iexact=value)

    def filter_by_tags(self, queryset: QuerySet, _name: str, value: str) -> QuerySet:
        """Filtre par plusieurs tags (separes par virgule)."""
        tag_names = [t.strip() for t in value.split(",")]
        return queryset.filter(tags__name__in=tag_names).distinct()


class CategoryFilter(django_filters.FilterSet):
    """Filtre pour les categories d'articles."""

    name = django_filters.CharFilter(lookup_expr="icontains")
    has_articles = django_filters.BooleanFilter(method="filter_has_articles")

    class Meta:
        model = Category
        fields = ["name", "slug"]

    def filter_has_articles(
        self,
        queryset: QuerySet,
        _name: str,
        value: bool,  # noqa: FBT001
    ) -> QuerySet:
        """Filtre les categories ayant des articles publies."""
        if value:
            return queryset.filter(articles__is_published=True).distinct()
        return queryset.exclude(articles__is_published=True)


class TagFilter(django_filters.FilterSet):
    """Filtre pour les tags d'articles."""

    name = django_filters.CharFilter(lookup_expr="icontains")
    has_articles = django_filters.BooleanFilter(method="filter_has_articles")

    class Meta:
        model = Tag
        fields = ["name"]

    def filter_has_articles(
        self,
        queryset: QuerySet,
        _name: str,
        value: bool,  # noqa: FBT001
    ) -> QuerySet:
        """Filtre les tags ayant des articles publies."""
        if value:
            return queryset.filter(articles__is_published=True).distinct()
        return queryset.exclude(articles__is_published=True)
