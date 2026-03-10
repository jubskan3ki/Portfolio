"""Mixins reutilisables pour les modeles Django."""

from typing import Any

from django.db import models
from django.db.models import Count, QuerySet
from django.utils.text import slugify

from utils.images import MAX_SIZE_LARGE, optimize_image


class WithItemCountMixin:
    """Mixin pour les managers de categories/statuts qui annotent un count.

    Usage:
        class ProjectCategoryManager(WithItemCountMixin, models.Manager):
            item_count_related_name = "projects"
    """

    item_count_related_name: str

    def with_item_count(self) -> QuerySet:
        """Annote avec le nombre d'items lies."""
        annotation_name = f"{self.item_count_related_name}_count"
        return self.get_queryset().annotate(  # type: ignore[attr-defined]
            **{annotation_name: Count(self.item_count_related_name)}
        )


class AutoSlugMixin(models.Model):
    """Mixin qui genere automatiquement le slug a partir d'un champ source.

    Usage:
        class MyModel(AutoSlugMixin, models.Model):
            slug_source_field = "name"  # or "title"
            name = models.CharField(max_length=100)
            slug = models.SlugField(unique=True, blank=True)
    """

    slug: models.SlugField  # type: ignore[assignment]
    slug_source_field: str = "name"

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            source = getattr(self, self.slug_source_field, "")
            self.slug = slugify(source)
        super().save(*args, **kwargs)


class OptimizeImageMixin(models.Model):
    """Mixin qui optimise automatiquement les images au save (WebP, resize).

    Usage:
        class MyModel(OptimizeImageMixin, models.Model):
            image_fields = {"image": MAX_SIZE_LARGE}
            image = models.ImageField(...)
    """

    image_fields: dict[str, tuple[int, int]] = {}

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        for field_name, max_size in self.image_fields.items():
            field = getattr(self, field_name, None)
            if field:
                optimize_image(field, max_size=max_size)
        super().save(*args, **kwargs)
