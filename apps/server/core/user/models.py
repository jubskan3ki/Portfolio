"""Modele utilisateur personnalise."""

from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from utils.images import MAX_SIZE_SMALL, optimize_image
from utils.validators import validate_image_upload

from .managers import ResetPasswordCodeManager, UserManager


def user_avatar_upload_to(instance, filename):
    """Determine le chemin de stockage pour l'avatar."""
    user_slug = slugify(instance.email.split("@")[0])
    return f"avatars/{user_slug}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    """Utilisateur personnalise avec email comme identifiant unique."""

    email = models.EmailField(_("adresse email"), unique=True, db_index=True)
    first_name = models.CharField(_("prenom"), max_length=150, blank=True)
    last_name = models.CharField(_("nom"), max_length=150, blank=True)
    phone_number = models.CharField(_("numero telephone"), max_length=15, blank=True, null=True)

    bio = models.TextField(_("biographie"), blank=True)
    avatar = models.ImageField(
        upload_to=user_avatar_upload_to, blank=True, null=True, validators=[validate_image_upload]
    )
    position = models.CharField(_("poste"), max_length=255, blank=True)

    public_email = models.EmailField(_("email public"), blank=True, null=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True, null=True)
    github = models.URLField(_("GitHub"), blank=True, null=True)
    twitter = models.URLField(_("Twitter"), blank=True, null=True)

    is_active = models.BooleanField(_("actif"), default=True)
    is_staff = models.BooleanField(_("statut staff"), default=False)

    date_joined = models.DateTimeField(_("date inscription"), default=timezone.now)
    updated_at = models.DateTimeField(_("derniere mise a jour"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")
        db_table = "users"
        ordering = ["-date_joined"]
        constraints = [
            models.UniqueConstraint(
                fields=["is_superuser"],
                condition=models.Q(is_superuser=True),
                name="unique_superuser",
            ),
        ]

    def __str__(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        """Retourne le prenom et le nom."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        """Retourne le prenom."""
        return self.first_name

    def save(self, *args, **kwargs):
        """Empeche la creation de plusieurs superusers et optimise l'avatar."""
        if self.is_superuser and User.objects.filter(is_superuser=True).exclude(pk=self.pk).exists():
            raise DjangoValidationError("Un seul superuser peut exister.")
        if self.avatar:
            optimize_image(self.avatar, max_size=MAX_SIZE_SMALL)
        super().save(*args, **kwargs)


class ResetPasswordCode(models.Model):
    """Code de reinitialisation de mot de passe."""

    MAX_ATTEMPTS = 3
    EXPIRY_MINUTES = 10

    email = models.EmailField(unique=True, db_index=True)
    code = models.CharField(max_length=8)
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects: ResetPasswordCodeManager = ResetPasswordCodeManager()

    class Meta:
        db_table = "password_reset_codes"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["email", "code"], name="idx_reset_email_code"),
        ]

    def __str__(self) -> str:
        return f"Reset code for {self.email}"

    def is_expired(self) -> bool:
        """Verifie si le code est expire."""
        return now() > self.created_at + timedelta(minutes=self.EXPIRY_MINUTES)

    def is_locked(self) -> bool:
        """Verifie si le code est bloque apres trop d'essais."""
        return self.attempts >= self.MAX_ATTEMPTS

    def increment_attempts(self) -> None:
        """Incremente le compteur d'essais."""
        self.attempts += 1
        self.save(update_fields=["attempts"])
