"""
Modèle de gestion des expériences (professionnelles & éducatives).
"""

from django.db import models


def experience_logo_upload_to(filename):
    return f"media/experience/{filename}"


class ExperienceManager(models.Manager):
    """
    Manager personnalisé pour la gestion des expériences.
    """

    def get_queryset(self):
        return super().get_queryset().order_by("-start_date")


class Experience(models.Model):
    """
    Modèle représentant une expérience (travail ou formation).
    """

    EXPERIENCE_TYPES = [
        ("work", "Expérience professionnelle"),
        ("education", "Formation / Diplôme"),
    ]

    title = models.CharField(max_length=255)
    company_or_school = models.CharField(max_length=255, help_text="Nom de l'entreprise ou de l'école")
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
        ordering = ["-start_date"]
        db_table = "experiences"

    def __str__(self) -> str:
        return f"{self.title} - {self.company_or_school}"
