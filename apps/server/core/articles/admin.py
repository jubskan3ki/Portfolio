"""Administration des articles."""

from django.contrib import admin
from django.db.models import Count, Q, QuerySet
from django.http import HttpRequest
from django.utils import timezone

from .models import Article, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin pour les categories d'articles."""

    list_display = ("name", "get_article_count", "slug")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request: HttpRequest) -> QuerySet[Category]:
        """Annote le nombre d'articles publies pour eviter les N+1."""
        return (
            super()
            .get_queryset(request)
            .annotate(published_article_count=Count("articles", filter=Q(articles__is_published=True)))
        )

    @admin.display(description="Nombre d'articles")
    def get_article_count(self, obj: Category) -> int:
        """Nombre d'articles dans cette categorie."""
        return obj.published_article_count  # type: ignore[attr-defined]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin pour les tags d'articles."""

    list_display = ("name", "get_article_count")
    search_fields = ("name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Tag]:
        """Annote le nombre d'articles publies pour eviter les N+1."""
        return (
            super()
            .get_queryset(request)
            .annotate(published_article_count=Count("articles", filter=Q(articles__is_published=True)))
        )

    @admin.display(description="Nombre d'articles")
    def get_article_count(self, obj: Tag) -> int:
        """Nombre d'articles avec ce tag."""
        return obj.published_article_count  # type: ignore[attr-defined]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin pour les articles."""

    list_display = (
        "title",
        "category",
        "published_date",
        "is_published",
        "is_featured",
        "view_count",
        "read_time",
    )
    list_select_related = ("category",)
    list_filter = ("is_published", "is_featured", "category", "published_date")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
    filter_horizontal = ("tags",)
    readonly_fields = ("view_count", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "content", "image")}),
        ("Categorisation", {"fields": ("category", "tags", "read_time")}),
        ("Publication", {"fields": ("is_published", "is_featured", "published_date")}),
        ("Statistiques", {"fields": ("view_count", "created_at", "updated_at")}),
    )
    actions = ["publish_articles", "unpublish_articles", "feature_articles", "unfeature_articles"]

    @admin.action(description="Publier les articles selectionnes")
    def publish_articles(self, request: HttpRequest, queryset: QuerySet[Article]) -> None:
        """Publie les articles selectionnes."""
        updated = queryset.update(is_published=True, published_date=timezone.now())
        self.message_user(request, f"{updated} article(s) publie(s).")

    @admin.action(description="Depublier les articles selectionnes")
    def unpublish_articles(self, request: HttpRequest, queryset: QuerySet[Article]) -> None:
        """Depublie les articles selectionnes."""
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} article(s) depublie(s).")

    @admin.action(description="Mettre en avant les articles selectionnes")
    def feature_articles(self, request: HttpRequest, queryset: QuerySet[Article]) -> None:
        """Met en avant les articles selectionnes."""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} article(s) mis en avant.")

    @admin.action(description="Retirer des articles mis en avant")
    def unfeature_articles(self, request: HttpRequest, queryset: QuerySet[Article]) -> None:
        """Retire les articles selectionnes des articles mis en avant."""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} article(s) retire(s) des articles mis en avant.")
