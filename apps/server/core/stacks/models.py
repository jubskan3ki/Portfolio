"""
Modèle de gestion des technologies et stacks.
"""

from django.db import models


def stack_icon_upload_to(filename):
    return f"media/stacks/{filename}"


class StackManager(models.Manager):
    """
    Manager personnalisé pour la gestion des stacks.
    """

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")


class Stack(models.Model):
    """
    Modèle représentant une technologie utilisée dans le portfolio.
    """

    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("devops", "DevOps"),
        ("mobile", "Mobile"),
        ("other", "Autre"),
    ]

    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to=stack_icon_upload_to, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    proficiency = models.IntegerField(default=1, help_text="Niveau de maîtrise (1 à 5)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StackManager()

    class Meta:
        ordering = ["-created_at"]
        db_table = "stacks"

    def __str__(self) -> str:
        return str(self.name)
