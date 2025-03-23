"""
User admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ResetPasswordCode, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    User admin
    """

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "last_password_change",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "bio", "avatar")}),
        ("Dates", {"fields": ("last_login", "date_joined", "last_password_change")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(ResetPasswordCode)
class ResetPasswordCodeAdmin(admin.ModelAdmin):
    """
    Reset password code admin
    """

    list_display = ("email", "code", "created_at", "is_expired")
    readonly_fields = ("created_at", "is_expired")
    search_fields = ("email",)
