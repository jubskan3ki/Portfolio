"""Modeles pour le systeme de webhooks."""

import hashlib
import hmac
import secrets
import uuid
from typing import Any, ClassVar

from django.conf import settings
from django.db import models

from utils.validators import validate_webhook_url

from .managers import WebhookDeliveryManager, WebhookManager


class WebhookEventType(models.TextChoices):
    """Types d'evenements supportes."""

    # Articles
    ARTICLE_CREATED = "article.created", "Article cree"
    ARTICLE_UPDATED = "article.updated", "Article mis a jour"
    ARTICLE_DELETED = "article.deleted", "Article supprime"
    ARTICLE_PUBLISHED = "article.published", "Article publie"

    # Projects
    PROJECT_CREATED = "project.created", "Projet cree"
    PROJECT_UPDATED = "project.updated", "Projet mis a jour"
    PROJECT_DELETED = "project.deleted", "Projet supprime"

    # Experiences
    EXPERIENCE_CREATED = "experience.created", "Experience creee"
    EXPERIENCE_UPDATED = "experience.updated", "Experience mise a jour"
    EXPERIENCE_DELETED = "experience.deleted", "Experience supprimee"

    # Contact
    CONTACT_RECEIVED = "contact.received", "Message de contact recu"

    # Stacks
    STACK_CREATED = "stack.created", "Stack cree"
    STACK_UPDATED = "stack.updated", "Stack mis a jour"


class Webhook(models.Model):
    """Webhook enregistre pour recevoir des notifications."""

    name = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom descriptif du webhook",
    )
    url = models.URLField(
        max_length=500,
        verbose_name="URL",
        help_text="URL de destination du webhook",
        validators=[validate_webhook_url],
    )
    secret = models.CharField(
        max_length=64,
        verbose_name="Secret",
        help_text="Secret pour signer les requetes (HMAC-SHA256)",
        editable=False,
    )
    events = models.JSONField(
        default=list,
        verbose_name="Evenements",
        help_text="Liste des types d'evenements a envoyer",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Le webhook est-il actif ?",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="webhooks",
        verbose_name="Cree par",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de creation",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification",
    )

    # Stats
    total_deliveries = models.PositiveIntegerField(
        default=0,
        verbose_name="Total livraisons",
    )
    successful_deliveries = models.PositiveIntegerField(
        default=0,
        verbose_name="Livraisons reussies",
    )
    last_delivery_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Derniere livraison",
    )

    objects: WebhookManager = WebhookManager()

    class Meta:
        verbose_name = "Webhook"
        verbose_name_plural = "Webhooks"
        db_table = "webhooks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.url})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Genere un secret si nouveau webhook."""
        if not self.secret:
            self.secret = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def generate_signature(self, payload: str) -> str:
        """Genere la signature HMAC-SHA256 pour le payload."""
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

    def is_subscribed_to(self, event_type: str) -> bool:
        """Verifie si le webhook est abonne a un type d'evenement."""
        if not self.is_active:
            return False
        return event_type in self.events or "*" in self.events


class WebhookDelivery(models.Model):
    """Historique des livraisons de webhooks."""

    class Status(models.TextChoices):
        """Status de livraison."""

        PENDING = "pending", "En attente"
        SUCCESS = "success", "Succes"
        FAILED = "failed", "Echec"
        RETRYING = "retrying", "Nouvelle tentative"

    webhook = models.ForeignKey(
        Webhook,
        on_delete=models.CASCADE,
        related_name="deliveries",
        verbose_name="Webhook",
    )
    event_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="ID evenement",
        help_text="Identifiant unique pour la deduplication",
    )
    event_type = models.CharField(
        max_length=50,
        choices=WebhookEventType.choices,
        verbose_name="Type d'evenement",
    )
    payload = models.JSONField(
        verbose_name="Payload",
        help_text="Donnees envoyees",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )
    response_status = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Code HTTP reponse",
    )
    response_body = models.TextField(
        blank=True,
        verbose_name="Corps de la reponse",
    )
    attempts = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Tentatives",
    )
    max_attempts: ClassVar[int] = 3
    next_retry_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Prochaine tentative",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de creation",
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de livraison",
    )
    duration_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Duree (ms)",
    )

    objects: WebhookDeliveryManager = WebhookDeliveryManager()

    class Meta:
        verbose_name = "Livraison webhook"
        verbose_name_plural = "Livraisons webhooks"
        db_table = "webhook_deliveries"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["webhook", "-created_at"]),
            models.Index(fields=["event_type"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["webhook", "event_id"],
                name="unique_webhook_event_id",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} -> {self.webhook.name} ({self.status})"

    def should_retry(self) -> bool:
        """Verifie si une nouvelle tentative est possible."""
        return self.status == self.Status.FAILED and self.attempts < self.max_attempts
