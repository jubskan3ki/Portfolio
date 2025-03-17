"""
Modèle de gestion des messages de contact.
"""

from django.db import models


class ContactMessageManager(models.Manager):
    """
    Manager personnalisé pour la gestion des messages de contact.
    """

    def get_queryset(self):
        """
        Récupère les messages de contact triés par date de création décroissante.
        """
        return super().get_queryset().order_by("-created_at")


class ContactMessage(models.Model):
    """
    Modèle représentant un message de contact soumis par un utilisateur.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ContactMessageManager()

    class Meta:
        """
        Métadonnées du modèle.
        """

        ordering = ["-created_at"]
        db_table = "contact_messages"

    def __str__(self) -> str:
        return f"Message de {self.name} ({self.email})"
