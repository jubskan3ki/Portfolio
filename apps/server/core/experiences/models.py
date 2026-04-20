"""Modeles pour la gestion des experiences professionnelles."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from utils.images import MAX_SIZE_SMALL
from utils.models import OptimizeImageMixin
from utils.upload import make_upload_to
from utils.validators import validate_image_upload

from .managers import ExperienceManager, ExperienceTypeManager

if TYPE_CHECKING:
    from django.db.models import QuerySet

    # Type alias for related managers
    RelatedManager = QuerySet


experience_logo_upload_to = make_upload_to("experiences", ("company", "title"))


def _format_date(date_field: Any, fmt: str) -> str:
    """Formate un champ date Django."""
    return date_field.strftime(fmt) if date_field else ""


def _get_year(date_field: Any) -> int | None:
    """Retourne l'annee d'un champ date Django."""
    return date_field.year if date_field else None


def _get_month(date_field: Any) -> int | None:
    """Retourne le mois d'un champ date Django."""
    return date_field.month if date_field else None


class ExperienceType(models.Model):
    """Type d'experience (ex: professionnel, education)."""

    id: int
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    objects: ExperienceTypeManager = ExperienceTypeManager()

    if TYPE_CHECKING:
        experiences: RelatedManager[Experience]

    class Meta:
        verbose_name = "Type d'experience"
        verbose_name_plural = "Types d'experiences"
        db_table = "experience_types"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class Experience(OptimizeImageMixin, models.Model):
    """Modele representant une experience professionnelle ou educative."""

    image_fields = {"logo": MAX_SIZE_SMALL}

    id: int
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    period = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    logo = models.ImageField(
        upload_to=experience_logo_upload_to, blank=True, null=True, validators=[validate_image_upload]
    )
    technologies = models.JSONField(default=list, blank=True)
    achievements = models.JSONField(default=list, blank=True)
    type = models.ForeignKey(
        ExperienceType,
        on_delete=models.PROTECT,
        related_name="experiences",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True, editable=False)

    objects: ExperienceManager = ExperienceManager()

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        db_table = "experiences"
        ordering = ["-start_date", "title"]
        indexes = [
            models.Index(fields=["start_date"]),
            models.Index(fields=["type"]),
            models.Index(fields=["end_date"]),
            models.Index(fields=["company"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} - {self.company}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Surcharge de save pour mettre a jour automatiquement le champ period."""
        if self.start_date:
            start_str = _format_date(self.start_date, "%b %Y")
            end_str = "Present" if not self.end_date else _format_date(self.end_date, "%b %Y")
            self.period = f"{start_str} - {end_str}"
        super().save(*args, **kwargs)

    def clean(self) -> None:
        """Valide la coherence des dates."""
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "La date de fin ne peut pas preceder la date de debut."})

    @property
    def year(self) -> int | None:
        """Retourne l'annee de debut de l'experience."""
        return _get_year(self.start_date)

    @property
    def is_current(self) -> bool:
        """Indique si l'experience est en cours."""
        return self.end_date is None

    @property
    def start_date_iso(self) -> str | None:
        """Retourne la date de debut au format ISO."""
        return _format_date(self.start_date, "%Y-%m-%d") or None

    @property
    def end_date_iso(self) -> str | None:
        """Retourne la date de fin au format ISO."""
        return _format_date(self.end_date, "%Y-%m-%d") or None

    @property
    def duration_months(self) -> int:
        """Calcule la duree de l'experience en mois."""
        if not self.start_date:
            return 0

        end_date: date = self.end_date or now().date()
        start_year = _get_year(self.start_date) or 0
        start_month = _get_month(self.start_date) or 0
        end_year = _get_year(end_date) or 0
        end_month = _get_month(end_date) or 0

        return (end_year - start_year) * 12 + (end_month - start_month)
