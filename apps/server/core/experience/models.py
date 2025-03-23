"""
Modèle de gestion des expériences (professionnelles & éducatives).
"""

from datetime import date
from typing import Optional

from django.db import models
from django.utils.text import slugify


def experience_logo_upload_to(instance, filename):
    """
    Chemin dynamique d'upload basé sur le nom de l'entreprise ou école.
    """
    slug = slugify(instance.company_or_school or "unknown")
    return f"experience/{slug}/{filename}"


class ExperienceManager(models.Manager):
    """
    Manager personnalisé enrichi pour gérer les expériences.
    """

    def get_queryset(self):
        """
        Retourne les expériences triées par date de début décroissante.
        """
        return super().get_queryset().order_by("-start_date")

    def professional(self):
        """
        Retourne uniquement les expériences professionnelles.
        """
        return self.get_queryset().filter(experience_type="work")

    def educational(self):
        """
        Retourne uniquement les formations et diplômes.
        """
        return self.get_queryset().filter(experience_type="education")

    def current(self):
        """
        Retourne les expériences actuellement en cours (sans date de fin).
        """
        return self.get_queryset().filter(end_date__isnull=True)


class Experience(models.Model):
    """
    Modèle complet représentant une expérience professionnelle ou éducative.
    """

    EXPERIENCE_TYPES = [
        ("work", "Expérience professionnelle"),
        ("education", "Formation / Diplôme"),
        ("internship", "Stage"),
        ("volunteer", "Bénévolat"),
        ("certification", "Certification"),
    ]

    title: str = models.CharField(max_length=255)
    company_or_school: str = models.CharField(max_length=255, help_text="Entreprise, école ou organisation")
    slug: str = models.SlugField(max_length=255, unique=True, blank=True)
    location: Optional[str] = models.CharField(max_length=255, blank=True, null=True)
    start_date: date = models.DateField()
    end_date: Optional[date] = models.DateField(blank=True, null=True)
    description: Optional[str] = models.TextField(blank=True)
    skills_acquired: list = models.JSONField(default=list, blank=True, help_text="Compétences acquises")
    experience_type: str = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    is_highlighted: bool = models.BooleanField(default=False, help_text="Expérience mise en avant dans le portfolio")
    website: Optional[str] = models.URLField(blank=True, null=True, help_text="Site web de l'entreprise ou école")
    logo = models.ImageField(upload_to=experience_logo_upload_to, blank=True, null=True)
    created_at: date = models.DateTimeField(auto_now_add=True)
    updated_at: date = models.DateTimeField(auto_now=True)

    objects = ExperienceManager()

    class Meta:
        """
        Métadonnées du modèle.
        """

        ordering = ["-start_date"]
        db_table = "experiences"
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"

    def __str__(self) -> str:
        return f"{self.title} chez {self.company_or_school}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.company_or_school}")
            unique_slug = base_slug
            counter = 1
            while Experience.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def duration(self) -> int:
        """
        Renvoie la durée de l'expérience en mois.
        """
        end_date: date = self.end_date or date.today()
        start_date: date = self.start_date

        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    @property
    def is_current(self) -> bool:
        """
        Renvoie True si l'expérience est actuellement en cours.
        """
        return self.end_date is None or self.end_date >= date.today()
