"""Managers pour le module contact."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from core.contact.models import FAQ, Contact, ContactInfo


class ContactManager(models.Manager["Contact"]):
    """Manager pour les contacts."""

    def new(self) -> models.QuerySet[Contact]:
        """Contacts non traites."""
        return self.get_queryset().filter(status="new").order_by("-created_at")

    def responded(self) -> models.QuerySet[Contact]:
        """Contacts avec reponse."""
        return self.get_queryset().filter(status="responded").order_by("-response_date")


class FAQManager(models.Manager["FAQ"]):
    """Manager pour les FAQs."""

    def published(self) -> models.QuerySet[FAQ]:
        """FAQs publiees."""
        return self.get_queryset().filter(is_published=True).order_by("order", "question")


class ContactInfoManager(models.Manager["ContactInfo"]):
    """Manager pour les informations de contact."""

    def primary(self) -> ContactInfo | None:
        """Retourne l'info de contact primaire."""
        return self.get_queryset().filter(is_primary=True).first()
