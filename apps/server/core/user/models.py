"""
Modèles enrichis et optimisés pour les utilisateurs.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now, timedelta


def user_avatar_upload_to(instance, filename):
    """
    Chemin dynamique d'upload des avatars basé sur l'email utilisateur.
    """
    user_slug = slugify(instance.email.split("@")[0])
    return f"avatars/{user_slug}/{filename}"


class UserManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle User.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Crée et sauvegarde un utilisateur avec l'email et le mot de passe donnés.
        """
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et sauvegarde un superuser avec l'email et le mot de passe donnés.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Le superuser doit avoir is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Le superuser doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle personnalisé enrichi pour les utilisateurs.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_to, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_password_change = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Meta options."""

        db_table = "users"
        ordering = ("email",)

    def __str__(self) -> str:
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.is_superuser and User.objects.filter(is_superuser=True).exclude(pk=self.pk).exists():
            raise ValueError("Un seul superuser peut exister.")
        super().save(*args, **kwargs)


class ResetPasswordCode(models.Model):
    """
    Stocke un code temporaire pour la réinitialisation du mot de passe.
    """

    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        """Meta options."""

        db_table = "user_reset_password_codes"
        ordering = ("-created_at",)

    def is_expired(self):
        """
        Vérifie si le code est expiré (valide 10 minutes).
        """
        return now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"Code de réinitialisation pour {self.email}"
