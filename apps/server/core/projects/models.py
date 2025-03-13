"""
Modèle de gestion des projets du portfolio.
"""

from django.db import models


def project_image_upload_to(filename):
    return f"media/projects/{filename}"


class ProjectManager(models.Manager):
    """
    Manager personnalisé pour la gestion des projets.
    """

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")


class Project(models.Model):
    """
    Modèle représentant un projet dans le portfolio.
    """

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to=project_image_upload_to, blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    live_demo = models.URLField(blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()

    class Meta:
        ordering = ["-created_at"]
        db_table = "projects"

    def __str__(self) -> str:
        return str(self.title)
