"""
Modèle enrichi et optimisé pour la gestion complète des projets du portfolio.
"""

from django.db import models
from django.utils.text import slugify


def project_image_upload_to(instance, filename):
    """Chemin dynamique d'upload basé sur le titre du projet."""
    project_slug = slugify(instance.title)
    return f"projects/{project_slug}/{filename}"


class ProjectManager(models.Manager):
    """
    Manager personnalisé permettant des requêtes utiles fréquentes.
    """

    def get_queryset(self):
        """Renvoie les projets triés par date de création décroissante."""
        return super().get_queryset().order_by("-created_at")

    def with_tag(self, tag):
        """Renvoie les projets contenant un tag spécifique."""
        return self.get_queryset().filter(tags__icontains=tag)

    def recent(self, limit=5):
        """Renvoie les projets les plus récents, limité par défaut à 5."""
        return self.get_queryset()[:limit]


class Project(models.Model):
    """
    Modèle enrichi représentant un projet complet dans le portfolio.
    """

    STATUS_CHOICES = [
        ("planning", "Planification"),
        ("in_progress", "En cours"),
        ("completed", "Terminé"),
        ("archived", "Archivé"),
    ]

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to=project_image_upload_to, blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    live_demo = models.URLField(blank=True, null=True)
    tags = models.JSONField(default=list, blank=True, help_text="Liste de tags associés au projet")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")
    priority = models.PositiveSmallIntegerField(default=1, help_text="Priorité du projet (1 à 10)")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()

    class Meta:
        """
        Métadonnées enrichies du modèle Project.
        """

        ordering = ["-created_at"]
        db_table = "projects"
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """Renvoie True si le projet est en cours ou en planification."""
        return self.status in ["planning", "in_progress"]

    @property
    def duration(self):
        """Renvoie la durée du projet en jours, si les dates sont définies."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None
