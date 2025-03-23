"""
Modèle de gestion des articles de blog.
"""

from django.db import models
from django.utils.text import slugify


def blog_image_upload_to(instance, filename):
    """
    Chemin dynamique d'upload des images basé sur le titre de l'article.
    """
    slug = slugify(instance.title)
    return f"blog/{slug}/{filename}"


class BlogPostManager(models.Manager):
    """
    Manager personnalisé enrichi pour gérer efficacement les articles de blog.
    """

    def get_queryset(self):
        """
        Renvoie les articles triés par date de publication décroissante.
        """
        return super().get_queryset().order_by("-published_at")

    def published(self):
        """
        Renvoie uniquement les articles publiés.
        """
        return self.get_queryset().filter(status="published")

    def drafts(self):
        """
        Renvoie uniquement les brouillons.
        """
        return self.get_queryset().filter(status="draft")

    def by_category(self, category):
        """
        Renvoie les articles filtrés par catégorie.
        """
        return self.get_queryset().filter(category__iexact=category)

    def recent(self, limit=5):
        """
        Renvoie les articles récents, limités à un nombre spécifié.
        """
        return self.published()[:limit]


class BlogPost(models.Model):
    """
    Modèle enrichi représentant un article de blog complet.
    """

    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publié"),
        ("archived", "Archivé"),
    ]

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to=blog_image_upload_to, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(blank=True, null=True)
    meta_description = models.CharField(
        max_length=160, blank=True, null=True, help_text="Description pour le référencement SEO."
    )
    seo_keywords = models.JSONField(default=list, blank=True, help_text="Mots-clés pour optimiser le SEO.")
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        """
        Métadonnées enrichies du modèle.
        """

        ordering = ["-published_at", "-created_at"]
        db_table = "blog_posts"
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        indexes = [
            models.Index(fields=["slug"], name="slug_idx"),
            models.Index(fields=["status"], name="status_idx"),
            models.Index(fields=["category"], name="category_idx"),
        ]

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == "published" and self.published_at is None:
            self.published_at = models.DateTimeField().to_python("now")
        super().save(*args, **kwargs)

    @property
    def is_published(self) -> bool:
        """
        Renvoie True si l'article est publié.
        """
        return self.status == "published"
