"""Modeles pour la gestion des articles de blog."""

from __future__ import annotations

from django.contrib.postgres.search import SearchVectorField
from django.db import models

from core.versioning.models import SoftDeleteAllManager, SoftDeleteMixin
from utils.images import MAX_SIZE_LARGE
from utils.models import AutoSlugMixin, OptimizeImageMixin
from utils.upload import make_upload_to
from utils.validators import validate_image_upload

from .managers import ArticleManager, CategoryManager, TagManager

article_image_upload_to = make_upload_to("article", "title", fallback="article")


class Category(AutoSlugMixin, models.Model):
    """Categorie d'articles."""

    id: int
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    # Annotation added by CategoryQuerySet.with_article_count()
    published_count: int

    objects: CategoryManager = CategoryManager()

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        db_table = "article_categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)

    @property
    def article_count(self) -> int:
        """Retourne le nombre d'articles publies dans cette categorie.

        Uses 'published_count' annotation when available (list/retrieve).
        Falls back to 0 for single-object responses (create/update)
        where annotation is not present.
        """
        if hasattr(self, "published_count"):
            return self.published_count
        return 0


class Tag(models.Model):
    """Tag d'article."""

    id: int
    name = models.CharField(max_length=50, unique=True)

    # Annotations added by TagQuerySet.with_article_count() / with_view_count_sum()
    published_count: int
    view_count_sum: int | None

    objects: TagManager = TagManager()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "article_tags"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)

    @property
    def article_count(self) -> int:
        """Retourne le nombre d'articles publies avec ce tag.

        Uses 'published_count' annotation when available (list/retrieve).
        Falls back to 0 for single-object responses (create/update)
        where annotation is not present.
        """
        if hasattr(self, "published_count"):
            return self.published_count
        return 0

    @property
    def total_view_count(self) -> int:
        """Retourne la somme des vues des articles publies lies a ce tag.

        Uses 'view_count_sum' annotation when available (list/retrieve).
        Falls back to 0 for single-object responses (create/update).
        """
        if hasattr(self, "view_count_sum"):
            return self.view_count_sum or 0
        return 0


class Article(OptimizeImageMixin, AutoSlugMixin, SoftDeleteMixin):
    """Article de blog."""

    slug_source_field = "title"
    image_fields = {"image": MAX_SIZE_LARGE}

    id: int
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    seo_title = models.CharField(
        max_length=70, blank=True, help_text="Titre SEO (max 70 car.). Utilise le titre si vide."
    )
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="Meta description (max 160 car.). Utilise l'extrait si vide."
    )
    excerpt = models.TextField()
    content = models.JSONField(default=list)
    image = models.ImageField(
        upload_to=article_image_upload_to, blank=True, null=True, validators=[validate_image_upload]
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles")
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)
    read_time = models.PositiveIntegerField(default=5)
    view_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
    search_vector = SearchVectorField(null=True, editable=False)

    objects: ArticleManager = ArticleManager()
    all_objects = SoftDeleteAllManager()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table = "articles"
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["published_date"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_published", "-published_date"]),
            models.Index(fields=["category", "is_published", "-published_date"]),
            models.Index(fields=["is_featured", "is_published", "-published_date"]),
        ]

    def __str__(self) -> str:
        return str(self.title)

    @property
    def tag_list(self) -> list[str]:
        """Retourne la liste des noms des tags associes a l'article."""
        # Use prefetched tags if available (prevents N+1 queries)
        if "tags" in getattr(self, "_prefetched_objects_cache", {}):
            return [tag.name for tag in self.tags.all()]
        return list(self.tags.values_list("name", flat=True))
