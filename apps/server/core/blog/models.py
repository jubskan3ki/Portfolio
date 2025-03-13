"""
Modèle de gestion des articles de blog.
"""

from django.db import models


def blog_image_upload_to(filename):
    return f"media/blog/{filename}"


class BlogPostManager(models.Manager):
    """
    Manager pour gérer les articles de blog.
    """

    def get_queryset(self):
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
        ordering = ["-created_at"]
        db_table = "blog_posts"

    def __str__(self) -> str:
        """Retourne le titre sous forme de chaîne de caractères."""
        return str(self.title)
