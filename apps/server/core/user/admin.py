"""Administration du module User."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import ResetPasswordCode, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin pour le modele utilisateur personnalise."""

    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Informations personnelles"), {"fields": ("first_name", "last_name")}),
        (_("Profil"), {"fields": ("phone_number", "bio", "avatar", "position")}),
        (_("Contacts publics"), {"fields": ("public_email", "linkedin", "github")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Dates importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    readonly_fields = ("date_joined", "last_login")


@admin.register(ResetPasswordCode)
class ResetPasswordCodeAdmin(admin.ModelAdmin):
    """Admin pour les codes de reinitialisation."""

    list_display = ("email", "code", "created_at", "is_expired")
    search_fields = ("email",)
    readonly_fields = ("created_at", "is_expired")
