"""Modeles de donnees pour les projets."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from django.contrib.postgres.search import SearchVectorField
from django.db import models

from utils.images import MAX_SIZE_LARGE
from utils.models import AutoSlugMixin, OptimizeImageMixin
from utils.upload import make_upload_to
from utils.validators import validate_image_upload

from .managers import ProjectCategoryManager, ProjectManager, ProjectStatusManager

if TYPE_CHECKING:
    from django.db.models import QuerySet

    # Type alias for related managers
    RelatedManager = QuerySet


project_image_upload_to = make_upload_to("projets", "title")


class ProjectCategory(AutoSlugMixin, models.Model):
    """Categorie de projets."""

    id: int
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    objects: ProjectCategoryManager = ProjectCategoryManager()

    if TYPE_CHECKING:
        projects: RelatedManager[Project]

    class Meta:
        verbose_name = "Categorie de projet"
        verbose_name_plural = "Categories de projets"
        db_table = "project_categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class ProjectStatus(models.Model):
    """Statut d'un projet."""

    id: int
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    objects: ProjectStatusManager = ProjectStatusManager()

    if TYPE_CHECKING:
        projects: RelatedManager[Project]

    class Meta:
        verbose_name = "Statut de projet"
        verbose_name_plural = "Statuts de projets"
        db_table = "project_status"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class Project(OptimizeImageMixin, AutoSlugMixin, models.Model):
    """Modele representant un projet."""

    slug_source_field = "title"
    image_fields = {"image": MAX_SIZE_LARGE}

    id: int
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    seo_title = models.CharField(
        max_length=70, blank=True, help_text="Titre SEO (max 70 car.). Utilise le titre si vide."
    )
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="Meta description (max 160 car.). Utilise la description si vide."
    )
    description = models.TextField()
    long_description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=project_image_upload_to, blank=True, null=True, validators=[validate_image_upload]
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        related_name="projects",
    )
    status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
        blank=True,
    )
    technologies = models.JSONField(default=list)
    features = models.JSONField(default=list, blank=True)
    links = models.JSONField(
        default=dict,
        blank=True,
        help_text="Format JSON: {'demo': 'url', 'github': 'url', 'documentation': 'url'}",
    )

    date = models.DateField(default=date.today)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True, editable=False)

    objects: ProjectManager = ProjectManager()

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        db_table = "projects"
        ordering = ["-date", "title"]
        indexes = [
            # slug UNIQUE (couvert par projects_slug_key + _like)
            # category / status FK couverts par auto index Django (couverts aussi par les composites ci-dessous)
            models.Index(fields=["date"]),
            models.Index(fields=["-view_count"]),
            models.Index(fields=["category", "-date"]),
            models.Index(fields=["status", "-date"]),
        ]

    def __str__(self) -> str:
        return str(self.title)

    @property
    def view(self) -> int:
        """Alias pour view_count pour correspondre a l'interface TS."""
        return self.view_count
