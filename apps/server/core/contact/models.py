"""
Modèle de gestion des messages de contact.
"""

from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessageManager(models.Manager):
    """
    Manager personnalisé enrichi pour la gestion des messages de contact.
    """

    def get_queryset(self):
        """
        Retourne les messages triés par date de création décroissante.
        """
        return super().get_queryset().order_by("-created_at")

    def unread(self):
        """
        Retourne uniquement les messages non lus.
        """
        return self.get_queryset().filter(is_read=False)

    def recent(self, limit=5):
        """
        Retourne les derniers messages reçus, limités à un nombre spécifié.
        """
        return self.get_queryset()[:limit]

    def by_email(self, email):
        """
        Retourne tous les messages provenant d'une adresse email spécifique.
        """
        return self.get_queryset().filter(email=email)


class ContactMessage(models.Model):
    """
    Modèle complet représentant un message reçu depuis le formulaire de contact.
    """

    SUBJECT_CHOICES = [
        ("general", "Général"),
        ("project", "Projet"),
        ("job", "Opportunité professionnelle"),
        ("support", "Support technique"),
        ("other", "Autre"),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name=_("Nom complet"),
        validators=[MinLengthValidator(2, _("Le nom doit contenir au moins 2 caractères."))],
    )

    email = models.EmailField(
        verbose_name=_("Adresse email"),
        validators=[
            RegexValidator(
                regex=r"^[\w\.-]+@[\w\.-]+\.\w+$",
                message=_("Veuillez fournir une adresse email valide."),
            )
        ],
    )

    subject = models.CharField(
        max_length=50, choices=SUBJECT_CHOICES, default="general", verbose_name=_("Sujet du message")
    )

    message = models.TextField(
        verbose_name=_("Contenu du message"),
        validators=[MinLengthValidator(10, _("Le message doit contenir au moins 10 caractères."))],
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Numéro de téléphone"),
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{8,15}$",
                message=_("Veuillez entrer un numéro de téléphone valide."),
            )
        ],
        help_text=_("Numéro de téléphone facultatif au format international."),
    )

    is_read = models.BooleanField(default=False, verbose_name=_("Lu ?"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de réception"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de dernière modification"))

    objects = ContactMessageManager()

    class Meta:
        """
        Métadonnées du modèle.
        """

        ordering = ["-created_at"]
        db_table = "contact_messages"
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["is_read"], name="read_status_idx"),
        ]

    def __str__(self) -> str:
        subject_display = getattr(self, "get_subject_display", lambda: self.subject)()
        return f"Message de {self.name} ({self.email}) - {subject_display}"

    def mark_as_read(self):
        """
        Marque le message comme lu.
        """
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read"])

    @property
    def short_message(self) -> str:
        """
        Renvoie un aperçu du message (50 caractères max).
        """
        message = str(self.message)
        return f"{message[:47]}..." if len(message) > 50 else message
