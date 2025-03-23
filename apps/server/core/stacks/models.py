"""
Modèle enrichi et optimisé de gestion des technologies et stacks.
"""

from django.db import models
from django.utils.text import slugify


def stack_icon_upload_to(instance, filename):
    """Chemin dynamique d'upload basé sur le nom de la stack."""
    name_slug = slugify(instance.name)
    return f"stacks/{name_slug}/{filename}"


class StackManager(models.Manager):
    """
    Manager personnalisé pour les stacks, permettant des requêtes courantes utiles.
    """

    def get_queryset(self):
        """
        Renvoie les stacks ordonnés par date de création décroissante.
        """
        return super().get_queryset().order_by("-created_at")

    def by_category(self, category):
        """
        Renvoie les stacks d'une catégorie spécifique.
        """
        return self.get_queryset().filter(category=category)

    def most_proficient(self):
        """
        Renvoie les stacks les plus maîtrisés, en priorisant le niveau de maîtrise.
        """
        return self.get_queryset().order_by("-proficiency", "-created_at")


class Stack(models.Model):
    """
    Modèle enrichi représentant une stack technologique complète dans le portfolio.
    """

    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("devops", "DevOps"),
        ("mobile", "Mobile"),
        ("cloud", "Cloud"),
        ("tools", "Outils"),
        ("other", "Autre"),
    ]

    PROFICIENCY_LEVELS = [
        (1, "Débutant"),
        (2, "Intermédiaire"),
        (3, "Avancé"),
        (4, "Expert"),
        (5, "Maîtrise Totale"),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.ImageField(upload_to=stack_icon_upload_to, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    proficiency = models.PositiveSmallIntegerField(
        choices=PROFICIENCY_LEVELS, default=1, help_text="Niveau de maîtrise (1 à 5)"
    )
    description = models.TextField(blank=True, null=True)
    official_website = models.URLField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0, help_text="Nombre d'années d'expérience")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StackManager()

    class Meta:
        """
        Métadonnées du modèle.
        """

        verbose_name = "Technologie / Stack"
        verbose_name_plural = "Technologies / Stacks"
        ordering = ["-created_at"]
        db_table = "stacks"

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def proficiency_label(self):
        """Renvoie le libellé du niveau de maîtrise."""
        return dict(self.PROFICIENCY_LEVELS).get(self.proficiency, "Non spécifié")
