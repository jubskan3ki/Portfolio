"""Managers personnalises pour les modeles d'articles."""

from __future__ import annotations

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db import models
from django.utils import timezone


def published_filter(prefix: str = "") -> models.Q:
    """Construit la condition ORM "article publie" reutilisable.

    Source unique du predicat : is_published=True ET (published_date NULL ou
    <= maintenant). `prefix` permet de cibler une relation inverse (ex:
    "articles__"). Coherent avec ArticleService._is_published (predicat applicatif).
    """
    now = timezone.now()
    return models.Q(**{f"{prefix}is_published": True}) & (
        models.Q(**{f"{prefix}published_date__isnull": True})
        | models.Q(**{f"{prefix}published_date__lte": now})
    )


class CategoryQuerySet(models.QuerySet):
    """QuerySet personnalise pour les categories d'articles."""

    def with_article_count(self) -> CategoryQuerySet:
        """Annote chaque categorie avec le nombre d'articles publies."""
        return self.annotate(
            published_count=models.Count(
                "articles",
                filter=published_filter("articles__"),
            )
        )

    def non_empty(self) -> CategoryQuerySet:
        """Retourne les categories ayant au moins un article publie."""
        return self.with_article_count().filter(published_count__gt=0)

    def ordered_by_name(self) -> CategoryQuerySet:
        """Tri par nom alphabetique."""
        return self.order_by("name")


class CategoryManager(models.Manager):
    """Manager pour les categories d'articles."""

    def get_queryset(self) -> CategoryQuerySet:
        return CategoryQuerySet(self.model, using=self._db)

    def with_article_count(self) -> CategoryQuerySet:
        return self.get_queryset().with_article_count()

    def non_empty(self) -> CategoryQuerySet:
        return self.get_queryset().non_empty()

    def ordered_by_name(self) -> CategoryQuerySet:
        return self.get_queryset().ordered_by_name()


class TagQuerySet(models.QuerySet):
    """QuerySet personnalise pour les tags d'articles."""

    def with_article_count(self) -> TagQuerySet:
        """Annote chaque tag avec le nombre d'articles publies."""
        return self.annotate(
            published_count=models.Count(
                "articles",
                filter=published_filter("articles__"),
            )
        )

    def with_view_count_sum(self) -> TagQuerySet:
        """Annote chaque tag avec la somme des vues des articles publies lies."""
        return self.annotate(
            view_count_sum=models.Sum(
                "articles__view_count",
                filter=published_filter("articles__"),
            )
        )

    def non_empty(self) -> TagQuerySet:
        """Retourne les tags ayant au moins un article publie."""
        return self.with_article_count().filter(published_count__gt=0)

    def ordered_by_name(self) -> TagQuerySet:
        """Tri par nom alphabetique."""
        return self.order_by("name")


class TagManager(models.Manager):
    """Manager pour les tags d'articles."""

    def get_queryset(self) -> TagQuerySet:
        return TagQuerySet(self.model, using=self._db)

    def with_article_count(self) -> TagQuerySet:
        return self.get_queryset().with_article_count()

    def with_view_count_sum(self) -> TagQuerySet:
        return self.get_queryset().with_view_count_sum()

    def non_empty(self) -> TagQuerySet:
        return self.get_queryset().non_empty()

    def ordered_by_name(self) -> TagQuerySet:
        return self.get_queryset().ordered_by_name()


class ArticleQuerySet(models.QuerySet):
    """QuerySet personnalise pour les articles."""

    def select_with_related(self) -> ArticleQuerySet:
        """Recupere les articles avec leurs relations."""
        return self.select_related("category").prefetch_related("tags")

    def published(self) -> ArticleQuerySet:
        """Filtre les articles publies (exclut les soft-deleted).

        Source ORM du predicat de publication (via published_filter). Coherent
        avec ArticleService._is_published : un article `is_published=True` sans
        `published_date` (NULL) est considere publie. Seul un `published_date`
        FUTUR (article programme) reste masque.
        """
        return self.filter(
            published_filter(),
            deleted_at__isnull=True,
        )

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

        search_vector = (
            SearchVector("title", weight="A", config=language)
            + SearchVector("excerpt", weight="B", config=language)
            + SearchVector("content", weight="C", config=language)
        )

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


class ArticleManager(models.Manager):
    """Manager pour les articles avec QuerySet personnalise."""

    def get_queryset(self) -> ArticleQuerySet:
        return ArticleQuerySet(self.model, using=self._db)

    def select_with_related(self) -> ArticleQuerySet:
        return self.get_queryset().select_with_related()

    def published(self) -> ArticleQuerySet:
        return self.get_queryset().published()

    def published_with_related(self) -> ArticleQuerySet:
        return self.get_queryset().published_with_related()

    def featured(self) -> ArticleQuerySet:
        return self.get_queryset().featured()

    def popular(self, limit: int = 5) -> ArticleQuerySet:
        return self.get_queryset().popular(limit)

    def recent(self, limit: int = 5) -> ArticleQuerySet:
        return self.get_queryset().recent(limit)

    def by_category(self, category_slug: str) -> ArticleQuerySet:
        return self.get_queryset().by_category(category_slug)

    def by_tag(self, tag_name: str) -> ArticleQuerySet:
        return self.get_queryset().by_tag(tag_name)

    def search(self, query: str) -> ArticleQuerySet:
        return self.get_queryset().search(query)

    def full_text_search(self, query: str, language: str = "french") -> ArticleQuerySet:
        return self.get_queryset().full_text_search(query, language)

    def similar_to(self, title: str, threshold: float = 0.3) -> ArticleQuerySet:
        return self.get_queryset().similar_to(title, threshold)
