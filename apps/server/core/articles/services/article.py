"""Service pour gerer les articles."""

from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Case, IntegerField, Q, QuerySet, Value, When
from django.utils import timezone

from config.constants import (
    DEFAULT_FEATURED_ARTICLES,
    DEFAULT_POPULAR_ARTICLES,
    DEFAULT_RELATED_ARTICLES,
)
from utils.cache.decorators import cached_queryset
from utils.cache.keys import CacheKeys
from utils.exceptions.service import NotFoundError
from utils.services import BaseService, apply_update, increment_view_count

from ..managers import ArticleQuerySet
from ..models import Article, Tag


class ArticleService(BaseService["Article"]):
    """Service pour les operations sur les articles."""

    model = Article
    entity_name = "Article"
    logger_name = "core.articles"

    ALLOWED_BLOCK_TYPES = {"paragraph", "heading", "blockquote", "image", "code", "list", "table"}

    @staticmethod
    def _normalize_heading(item: dict) -> dict | None:
        level = item.get("level", 2)
        return {
            "type": "heading",
            "content": str(item.get("content", "")),
            "level": level if level in (2, 3, 4) else 2,
        }

    @staticmethod
    def _normalize_blockquote(item: dict) -> dict | None:
        return {
            "type": "blockquote",
            "content": str(item.get("content", "")),
            **({"cite": str(item["cite"])} if item.get("cite") else {}),
        }

    @staticmethod
    def _normalize_image(item: dict) -> dict | None:
        src = item.get("src", "")
        if not src:
            return None
        return {
            "type": "image",
            "src": str(src),
            "alt": str(item.get("alt", "")),
            **({"caption": str(item["caption"])} if item.get("caption") else {}),
        }

    @staticmethod
    def _normalize_code(item: dict) -> dict | None:
        return {
            "type": "code",
            "content": str(item.get("content", "")),
            **({"language": str(item["language"])} if item.get("language") else {}),
        }

    @staticmethod
    def _normalize_list(item: dict) -> dict | None:
        items = item.get("items", [])
        if not isinstance(items, list):
            return None
        return {
            "type": "list",
            "items": [str(i) for i in items],
            "ordered": bool(item.get("ordered", False)),
        }

    @staticmethod
    def _normalize_table(item: dict) -> dict | None:
        headers = item.get("headers", [])
        rows = item.get("rows", [])
        if not isinstance(headers, list) or not isinstance(rows, list):
            return None
        return {
            "type": "table",
            "headers": [str(h) for h in headers],
            "rows": [[str(c) for c in row] for row in rows if isinstance(row, list)],
        }

    @staticmethod
    def _normalize_paragraph(item: dict) -> dict | None:
        content_val = str(item.get("content", ""))
        if not content_val.strip():
            return None
        return {"type": "paragraph", "content": content_val}

    @classmethod
    def validate_content_blocks(cls, content: list) -> list:
        """Valide et normalise une liste de blocs de contenu.

        Accepte un mix de strings (legacy) et de dicts (blocs structures).
        Les strings sont convertis en blocs paragraph.
        Le type legacy 'text' est normalise en 'paragraph'.
        """
        normalizers = {
            "paragraph": cls._normalize_paragraph,
            "heading": cls._normalize_heading,
            "blockquote": cls._normalize_blockquote,
            "image": cls._normalize_image,
            "code": cls._normalize_code,
            "list": cls._normalize_list,
            "table": cls._normalize_table,
        }

        normalized = []
        for item in content:
            if isinstance(item, str):
                if item.strip():
                    normalized.append({"type": "paragraph", "content": item})
                continue

            if not isinstance(item, dict):
                continue

            block_type = item.get("type", "")
            if block_type == "text":
                block_type = "paragraph"

            normalizer = normalizers.get(block_type)
            if not normalizer:
                continue

            block = normalizer(item)
            if block:
                normalized.append(block)

        return normalized

    @classmethod
    def _get_base_queryset(cls) -> QuerySet[Article]:
        """Queryset publié avec relations."""
        return Article.objects.published_with_related()

    @classmethod
    def _get_detail_queryset(cls) -> QuerySet[Article]:
        """Queryset complet avec relations (admin inclus)."""
        return Article.objects.select_with_related()

    @classmethod
    def get_all(cls, *, published_only: bool = True) -> QuerySet[Article]:
        """Recupere tous les articles."""
        if published_only:
            return cls._get_base_queryset()
        return cls._get_detail_queryset()

    @classmethod
    def _get_by(cls, *, published_only: bool = True, **lookup: Any) -> Article:
        """Recupere un article par un critere de recherche unique."""
        try:
            article = cls._get_detail_queryset().get(**lookup)
            if published_only and not cls._is_published(article):
                raise NotFoundError(f"Article {lookup} non publie.", details=lookup)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning("Article non trouve: %s", lookup)
            raise NotFoundError(f"Article {lookup} non trouve.", details=lookup) from exc
        return article

    @classmethod
    def get_by_id(cls, pk: int, *, published_only: bool = True) -> Article:  # type: ignore[override]
        """Recupere un article par son ID."""
        return cls._get_by(id=pk, published_only=published_only)

    @classmethod
    def get_by_slug(cls, slug: str, *, published_only: bool = True) -> Article:  # type: ignore[override]
        """Recupere un article par son slug."""
        return cls._get_by(slug=slug, published_only=published_only)

    @staticmethod
    def _is_published(article: Article) -> bool:
        """Verifie si un article est publie."""
        if not article.is_published:
            return False
        return not (article.published_date and article.published_date > timezone.now())

    @classmethod
    @transaction.atomic
    def create(cls, data: dict[str, Any]) -> Article:
        """Cree un nouvel article avec gestion automatique de la date de publication."""
        tags_data = data.pop("tags", None)

        is_published = data.get("is_published", False)
        if is_published and not data.get("published_date"):
            data["published_date"] = timezone.now()

        article = Article.objects.create(**data)

        if tags_data:
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)

        return article

    @classmethod
    @transaction.atomic
    def update(cls, pk: int, data: dict[str, Any], *, partial: bool = False) -> Article:  # type: ignore[override]
        """Met a jour un article avec gestion auto de la date de publication."""
        article = cls.get_by_id(pk, published_only=False)
        tags_data = data.pop("tags", None)

        is_published = data.get("is_published", article.is_published)
        if is_published and not article.published_date and not data.get("published_date"):
            data["published_date"] = timezone.now()

        apply_update(article, data, partial=partial)
        article.save()

        if tags_data is not None:
            article.tags.clear()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)

        return article

    @classmethod
    def delete(cls, pk: int) -> None:
        """Supprime un article."""
        article = cls.get_by_id(pk, published_only=False)
        article.delete()

    @classmethod
    @cached_queryset(
        lambda slug, **_kw: CacheKeys.make_key("articles", "category", slug),
        timeout=CacheKeys.TTL_MEDIUM,
    )
    def get_by_category(cls, category_slug: str, *, published_only: bool = True) -> QuerySet[Article]:
        """Recupere les articles d'une categorie specifique."""
        if published_only:
            return Article.objects.by_category(category_slug)
        return cls._get_detail_queryset().filter(category__slug=category_slug)

    @classmethod
    @cached_queryset(
        lambda tag, **_kw: CacheKeys.make_key("articles", "tag", tag),
        timeout=CacheKeys.TTL_MEDIUM,
    )
    def get_by_tag(cls, tag_name: str, *, published_only: bool = True) -> QuerySet[Article]:
        """Recupere les articles avec un tag specifique."""
        if published_only:
            return Article.objects.by_tag(tag_name)
        return cls._get_detail_queryset().filter(tags__name__iexact=tag_name)

    @classmethod
    @cached_queryset(
        lambda limit=DEFAULT_FEATURED_ARTICLES: CacheKeys.article_featured(limit),
        timeout=CacheKeys.TTL_MEDIUM,
    )
    def get_featured(cls, limit: int = DEFAULT_FEATURED_ARTICLES) -> ArticleQuerySet:
        """Recupere les articles mis en avant."""
        return Article.objects.featured()[:limit]

    @classmethod
    @cached_queryset(
        lambda limit=DEFAULT_POPULAR_ARTICLES: CacheKeys.article_popular(limit),
        timeout=CacheKeys.TTL_MEDIUM,
    )
    def get_popular(cls, limit: int = DEFAULT_POPULAR_ARTICLES) -> ArticleQuerySet:
        """Recupere les articles les plus populaires."""
        return Article.objects.popular(limit)

    @classmethod
    def get_related(cls, article: Article, limit: int = DEFAULT_RELATED_ARTICLES) -> list[Article]:
        """Recupere les articles similaires a un article donne (optimized single query)."""
        tag_ids = [t.id for t in article.tags.all()]

        if tag_ids:
            filter_condition = Q(category=article.category) | Q(tags__id__in=tag_ids)
        else:
            filter_condition = Q(category=article.category)

        queryset = (
            Article.objects.published_with_related()
            .exclude(id=article.id)
            .filter(filter_condition)
            .annotate(
                relevance=Case(
                    When(category=article.category, then=Value(2)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            .order_by("-relevance", "-published_date")
            .distinct()[:limit]
        )

        return list(queryset)

    @classmethod
    def increment_view_and_get(cls, article_slug: str) -> Article:
        """Incremente le compteur de vues et retourne l'article mis a jour."""
        from core.stats.models import ViewLog

        try:
            article = Article.objects.get(slug=article_slug)
        except ObjectDoesNotExist as exc:
            cls._get_logger().warning(
                "Article non trouve pour incrementer les vues: slug=%s",
                article_slug,
            )
            raise NotFoundError(
                f"Article '{article_slug}' non trouve.",
                details={"slug": article_slug},
            ) from exc

        increment_view_count(article)
        article.refresh_from_db(fields=["view_count"])
        ViewLog.objects.log_view("article", article.id)
        return article
