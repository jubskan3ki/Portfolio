"""Mixins reutilisables pour les modeles Django."""

from typing import Any

from django.db import models
from django.db.models import Count, QuerySet
from django.utils.text import slugify

from utils.images import optimize_image


class WithItemCountMixin:
    """Manager qui annote un count sur la related_name."""

    item_count_related_name: str

    def with_item_count(self) -> QuerySet:
        annotation_name = f"{self.item_count_related_name}_count"
        return self.get_queryset().annotate(  # type: ignore[attr-defined]
            **{annotation_name: Count(self.item_count_related_name)}
        )


class AutoSlugMixin(models.Model):
    """Genere slug depuis slug_source_field au save si vide."""

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
    """Resize + WebP pour chaque champ dans image_fields au save."""

    image_fields: dict[str, tuple[int, int]] = {}

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        for field_name, max_size in self.image_fields.items():
            field = getattr(self, field_name, None)
            if field:
                optimize_image(field, max_size=max_size)
        super().save(*args, **kwargs)
