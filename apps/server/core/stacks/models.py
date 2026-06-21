"""Modeles de donnees pour les stacks techniques."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from utils.models import AutoSlugMixin
from utils.security.svg import sanitize_svg_upload
from utils.upload import make_upload_to

from .managers import (
    StackCategoryManager,
    StackManager,
    StackRelationshipManager,
    StackResourceManager,
)

if TYPE_CHECKING:
    from django.db.models import QuerySet

    # Type alias for related managers
    RelatedManager = QuerySet


ALLOWED_LOGO_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]
ALLOWED_LOGO_TYPES = [
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/svg+xml",
]

RELATIONSHIP_TYPES = (
    ("alternative", "Alternative"),
    ("complementary", "Complementaire"),
    ("dependency", "Dependance"),
    ("similarTo", "Similaire"),
)

RESOURCE_TYPES = (
    ("documentation", "Documentation"),
    ("tutorial", "Tutoriel"),
    ("article", "Article"),
    ("video", "Video"),
    ("other", "Autre"),
)


def validate_logo_file(value: Any) -> None:
    """Valide que le fichier est une image ou un SVG."""
    from pathlib import Path

    if not value:
        return

    ext = Path(value.name).suffix.lower()
    if ext not in ALLOWED_LOGO_EXTENSIONS:
        raise ValidationError(
            f"Extension '{ext}' non autorisee. Extensions acceptees: {', '.join(ALLOWED_LOGO_EXTENSIONS)}"
        )

    content_type = getattr(value, "content_type", None)
    if content_type and content_type not in ALLOWED_LOGO_TYPES:
        raise ValidationError(f"Type de fichier '{content_type}' non autorise.")


stack_logo_upload_to = make_upload_to("stacks", "name")


class StackCategory(models.Model):
    """Categorie de technologies."""

    id: int
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    objects: StackCategoryManager = StackCategoryManager()

    if TYPE_CHECKING:
        stacks: RelatedManager[Stack]

    class Meta:
        verbose_name = "Categorie de stack"
        verbose_name_plural = "Categories de stacks"
        db_table = "stack_categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class Stack(AutoSlugMixin, models.Model):
    """Modele representant une technologie/stack."""

    id: int
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    seo_title = models.CharField(
        max_length=70, blank=True, help_text="Titre SEO (max 70 car.). Utilise le nom si vide."
    )
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="Meta description (max 160 car.). Utilise la description si vide."
    )
    description = models.TextField()
    logo = models.FileField(
        upload_to=stack_logo_upload_to,
        blank=True,
        null=True,
        validators=[validate_logo_file],
        help_text="Logo (PNG, JPG, GIF, WebP ou SVG)",
    )
    category = models.ForeignKey(
        StackCategory,
        on_delete=models.PROTECT,
        related_name="stacks",
    )
    tags = models.JSONField(default=list)
    started_date = models.DateField(
        help_text="Date de d\u00e9but d'utilisation de cette technologie",
        null=True,
        blank=True,
    )
    level = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Niveau de maitrise (0.5-5.0)",
        validators=[MinValueValidator(Decimal("0.5")), MaxValueValidator(Decimal("5.0"))],
        default=Decimal("0.5"),
    )
    website = models.URLField(blank=True, null=True)
    website_label = models.CharField(max_length=50, blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    github_label = models.CharField(max_length=50, blank=True, null=True)
    first_release = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=50, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True, editable=False)

    related_stacks_m2m: models.ManyToManyField = models.ManyToManyField(
        "self",
        through="StackRelationship",
        symmetrical=False,
        related_name="related_to",
    )

    objects: StackManager = StackManager()

    class Meta:
        verbose_name = "Stack technique"
        verbose_name_plural = "Stacks techniques"
        db_table = "stacks"
        ordering = ["-level", "name"]
        indexes = [
            models.Index(fields=["level"]),
        ]

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Assainit un logo SVG uploade (anti-XSS) avant la sauvegarde."""
        sanitize_svg_upload(self.logo)
        super().save(*args, **kwargs)

    @property
    def experience_months(self) -> int:
        """Calcule l'experience en mois depuis la date de debut."""
        if not self.started_date:
            return 0
        today = timezone.now().date()
        months = (today.year - self.started_date.year) * 12 + (today.month - self.started_date.month)
        return max(0, months)


class StackRelationship(models.Model):
    """Relation entre deux stacks."""

    id: int
    from_stack = models.ForeignKey(
        Stack,
        on_delete=models.CASCADE,
        related_name="relationships",
    )
    to_stack = models.ForeignKey(
        Stack,
        on_delete=models.CASCADE,
        related_name="related_from",
    )
    relationship_type = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_TYPES,
        default="similarTo",
    )

    objects: StackRelationshipManager = StackRelationshipManager()

    class Meta:
        verbose_name = "Relation entre stacks"
        verbose_name_plural = "Relations entre stacks"
        db_table = "stack_relationships"
        constraints = [
            models.UniqueConstraint(
                fields=["from_stack", "to_stack"],
                name="unique_stack_relationship",
            ),
            models.CheckConstraint(
                condition=~models.Q(from_stack=models.F("to_stack")),
                name="prevent_self_relationship",
            ),
        ]
        indexes = [
            models.Index(fields=["from_stack", "relationship_type"]),
            models.Index(fields=["to_stack"]),
        ]

    def __str__(self) -> str:
        return f"{self.from_stack.name} -> {self.relationship_type} -> {self.to_stack.name}"


class StackResource(models.Model):
    """Ressource liee a une stack (documentation, tutoriels, etc.)."""

    id: int
    stack = models.ForeignKey(
        Stack,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default="documentation")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects: StackResourceManager = StackResourceManager()

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        db_table = "stack_resources"
        ordering = ["-is_featured", "title"]
        indexes = [
            models.Index(fields=["stack", "type"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.stack.name})"
