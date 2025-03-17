"""
Modèle de gestion des articles de blog.
"""

from django.db import models
from django.utils.text import slugify


def blog_image_upload_to(instance, filename):
    """
    Chemin dynamique d'upload des images.
    """
    slug = slugify(instance.title)
    return f"blog/{slug}/{filename}"


class BlogPostManager(models.Manager):
    """
    Manager personnalisé pour gérer les articles de blog.
    """

    def get_queryset(self):
        """
        Renvoie les articles de blog triés par date de création décroissante.
        """
        return super().get_queryset().order_by("-created_at")


class BlogPost(models.Model):
    """
    Modèle représentant un article de blog.
    """

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to=blog_image_upload_to, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        """
        Métadonnées du modèle.
        """

        ordering = ["-created_at"]
        db_table = "blog_posts"

    def __str__(self) -> str:
        return str(self.title)
