"""
Modèles pour les utilisateurs.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.timezone import now, timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Le superuser doit avoir is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Le superuser doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.is_superuser and User.objects.filter(is_superuser=True).exclude(pk=self.pk).exists():
            raise ValueError("Un seul superuser peut exister.")
        super().save(*args, **kwargs)


class ResetPasswordCode(models.Model):
    """
    Stocke un code temporaire pour la réinitialisation du mot de passe de l'admin.
    """

    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = "user_reset_password_codes"

    def is_expired(self):
        """
        Vérifie si le code est expiré (valide 10 minutes).
        """
        return now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"Code de réinitialisation pour {self.email}"
