"""Managers personnalises pour les modeles d'articles."""

from __future__ import annotations

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db import models
from django.utils import timezone


class CategoryQuerySet(models.QuerySet):
    """QuerySet personnalise pour les categories d'articles."""

    def with_article_count(self) -> CategoryQuerySet:
        """Annote chaque categorie avec le nombre d'articles publies."""
        return self.annotate(
            published_count=models.Count(
                "articles",
                filter=models.Q(
                    articles__is_published=True,
                    articles__published_date__lte=timezone.now(),
                ),
            )
        )

    def non_empty(self) -> CategoryQuerySet:
        """Retourne les categories ayant au moins un article publie."""
        return self.with_article_count().filter(published_count__gt=0)

    def ordered_by_name(self) -> CategoryQuerySet:
        """Tri par nom alphabetique."""
        return self.order_by("name")


CategoryManager = models.Manager.from_queryset(CategoryQuerySet)


class TagQuerySet(models.QuerySet):
    """QuerySet personnalise pour les tags d'articles."""

    def with_article_count(self) -> TagQuerySet:
        """Annote chaque tag avec le nombre d'articles publies."""
        return self.annotate(
            published_count=models.Count(
                "articles",
                filter=models.Q(
                    articles__is_published=True,
                    articles__published_date__lte=timezone.now(),
                ),
            )
        )

    def with_view_count_sum(self) -> TagQuerySet:
        """Annote chaque tag avec la somme des vues des articles publies lies."""
        return self.annotate(
            view_count_sum=models.Sum(
                "articles__view_count",
                filter=models.Q(
                    articles__is_published=True,
                    articles__published_date__lte=timezone.now(),
                ),
            )
        )

    def non_empty(self) -> TagQuerySet:
        """Retourne les tags ayant au moins un article publie."""
        return self.with_article_count().filter(published_count__gt=0)

    def ordered_by_name(self) -> TagQuerySet:
        """Tri par nom alphabetique."""
        return self.order_by("name")


TagManager = models.Manager.from_queryset(TagQuerySet)


class ArticleQuerySet(models.QuerySet):
    """QuerySet personnalise pour les articles."""

    def select_with_related(self) -> ArticleQuerySet:
        """Recupere les articles avec leurs relations."""
        return self.select_related("category").prefetch_related("tags")

    def published(self) -> ArticleQuerySet:
        """Filtre les articles publies (exclut les soft-deleted)."""
        return self.filter(is_published=True, published_date__lte=timezone.now(), deleted_at__isnull=True)

    def published_with_related(self) -> ArticleQuerySet:
        """Filtre les articles publies avec leurs relations."""
        return self.published().select_with_related()

    def featured(self) -> ArticleQuerySet:
        """Filtre les articles mis en avant."""
        return self.published_with_related().filter(is_featured=True)

    def popular(self, limit: int = 5) -> ArticleQuerySet:
        """Retourne les articles les plus vus."""
        return self.published_with_related().order_by("-view_count")[:limit]

    def recent(self, limit: int = 5) -> ArticleQuerySet:
        """Retourne les articles les plus recents."""
        return self.published_with_related().order_by("-published_date")[:limit]

    def by_category(self, category_slug: str) -> ArticleQuerySet:
        """Filtre les articles par categorie."""
        return self.published_with_related().filter(category__slug=category_slug)

    def by_tag(self, tag_name: str) -> ArticleQuerySet:
        """Filtre les articles par tag."""
        return self.published_with_related().filter(tags__name__iexact=tag_name)

    def search(self, query: str) -> ArticleQuerySet:
        """Recherche des articles par mot-cle (fallback simple)."""
        return self.published_with_related().filter(
            models.Q(title__icontains=query) | models.Q(excerpt__icontains=query) | models.Q(content__icontains=query)
        )

    def full_text_search(self, query: str, language: str = "french") -> ArticleQuerySet:
        """Recherche Full-Text PostgreSQL avec ranking.

        Utilise SearchVector pour indexer titre, extrait et contenu.
        Les resultats sont tries par pertinence (SearchRank).

        Args:
            query: Terme de recherche
            language: Langue pour le stemming (default: french)

        Returns:
            QuerySet annote avec 'rank' et trie par pertinence
        """
        if not query or not query.strip():
            return self.none()

        # Vecteur de recherche avec poids differents (A = highest, D = lowest)
        search_vector = (
            SearchVector("title", weight="A", config=language)
            + SearchVector("excerpt", weight="B", config=language)
            + SearchVector("content", weight="C", config=language)
        )

        # Query de recherche avec configuration de langue
        search_query = SearchQuery(query, config=language)

        return (
            self.published_with_related()
            .annotate(
                rank=SearchRank(search_vector, search_query),
            )
            .filter(rank__gte=0.01)
            .order_by("-rank")
        )

    def similar_to(self, title: str, threshold: float = 0.3) -> ArticleQuerySet:
        """Trouve les articles avec des titres similaires (trigram).

        Utilise pg_trgm pour la similarite de texte.

        Args:
            title: Titre a comparer
            threshold: Seuil de similarite minimum (0-1)

        Returns:
            QuerySet annote avec 'similarity' et filtre par seuil
        """
        return (
            self.published_with_related()
            .annotate(similarity=TrigramSimilarity("title", title))
            .filter(similarity__gte=threshold)
            .order_by("-similarity")
        )


ArticleManager = models.Manager.from_queryset(ArticleQuerySet)
