"""Modeles pour la gestion des contacts et FAQs."""

from typing import Any

from django.db import models, transaction
from django.utils import formats

from .managers import ContactInfoManager, ContactManager, FAQManager


class FAQ(models.Model):
    """Modele pour les questions frequemment posees."""

    id: int
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: FAQManager = FAQManager()

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["order", "question"]
        db_table = "faq"
        indexes = [
            models.Index(fields=["is_published", "order"]),
        ]

    def __str__(self) -> str:
        return str(self.question)


class Contact(models.Model):
    """Modele pour enregistrer les soumissions de formulaire de contact."""

    STATUS_CHOICES = (
        ("new", "Nouveau"),
        ("responded", "Repondu"),
        ("closed", "Cloture"),
    )

    id: int
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    reference_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    response_message = models.TextField(blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: ContactManager = ContactManager()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        db_table = "contact"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["email"]),
            models.Index(fields=["reference_id"]),
            models.Index(fields=["ip_address"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        date_str = formats.date_format(self.created_at, format="SHORT_DATE_FORMAT")
        return f"{self.name} - {self.subject} ({date_str})"


class ContactInfo(models.Model):
    """Modele pour stocker les informations de contact."""

    AVAILABILITY_CHOICES = (
        ("available", "Disponible"),
        ("limited", "Disponibilite limitee"),
        ("unavailable", "Indisponible"),
    )

    id: int
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    medium = models.URLField(blank=True)
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available",
    )
    availability_message = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: ContactInfoManager = ContactInfoManager()

    class Meta:
        verbose_name = "Information de contact"
        verbose_name_plural = "Informations de contact"
        db_table = "contact_info"
        ordering = ["-is_primary", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["is_primary"],
                condition=models.Q(is_primary=True),
                name="unique_primary_contact_info",
            ),
        ]

    def __str__(self) -> str:
        return str(self.email)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Si marque comme primaire, desactive les autres comme primaires."""
        with transaction.atomic():
            if self.is_primary:
                # Verrouiller les lignes pour eviter les race conditions
                ContactInfo.objects.select_for_update().filter(is_primary=True).exclude(pk=self.pk).update(
                    is_primary=False
                )
            super().save(*args, **kwargs)
