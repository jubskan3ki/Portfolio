"""
Modèle de gestion des expériences (professionnelles & éducatives).
"""

from django.db import models
from django.utils.text import slugify


def experience_logo_upload_to(instance, filename):
    """
    Upload path unique basé sur le nom de l'entreprise/école.
    """
    slug = slugify(instance.company_or_school or "unknown")
    return f"experience/{slug}/{filename}"


class ExperienceManager(models.Manager):
    """
    Manager personnalisé pour les expériences.
    """

    def get_queryset(self):
        """
        Retourne les expériences triées par date de début (desc).
        """
        return super().get_queryset().order_by("-start_date")


class Experience(models.Model):
    """
    Modèle représentant une expérience (professionnelle ou éducative).
    """

    EXPERIENCE_TYPES = [
        ("work", "Expérience professionnelle"),
        ("education", "Formation / Diplôme"),
    ]

    title = models.CharField(max_length=255)
    company_or_school = models.CharField(max_length=255, help_text="Entreprise ou école")
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    logo = models.ImageField(upload_to=experience_logo_upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ExperienceManager()

    class Meta:
        """
        Métadonnées du modèle.
        """

        ordering = ["-start_date"]
        db_table = "experiences"

    def __str__(self):
        return f"{self.title} - {self.company_or_school}"
