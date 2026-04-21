"""Mixins reutilisables pour les modeles Django."""

from typing import TYPE_CHECKING, Any, cast

from django.db import models
from django.db.models import Count, QuerySet
from django.utils.text import slugify

from utils.images import optimize_image

if TYPE_CHECKING:

    class _HasGetQueryset:
        def get_queryset(self) -> QuerySet[Any]: ...


class WithItemCountMixin:
    """Manager qui annote un count sur la related_name."""

    item_count_related_name: str

    def with_item_count(self) -> QuerySet:
        annotation_name = f"{self.item_count_related_name}_count"
        manager_self = cast("_HasGetQueryset", self)
        return manager_self.get_queryset().annotate(**{annotation_name: Count(self.item_count_related_name)})


class AutoSlugMixin(models.Model):
    """Genere slug depuis slug_source_field au save si vide.

    Les sous-classes doivent declarer un champ `slug = models.SlugField(...)`.
    """

    slug_source_field: str = "name"

    class Meta:
        abstract = True

    if TYPE_CHECKING:
        slug: Any

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
