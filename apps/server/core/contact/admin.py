"""Configuration de l'administration pour le module de contact."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import SafeString

from .models import FAQ, Contact, ContactInfo


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Administration des FAQs."""

    list_display = ("question", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("question", "answer")
    list_editable = ("is_published", "order")
    fieldsets = (
        (None, {"fields": ("question", "answer", "order", "is_published")}),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Administration des informations de contact."""

    list_display = ("email", "is_primary", "availability_status", "updated_at")
    list_filter = ("availability_status", "is_primary")
    search_fields = ("email", "phone")
    list_editable = ("is_primary", "availability_status")
    fieldsets = (
        (None, {"fields": ("email", "phone", "is_primary")}),
        ("Adresse", {"fields": ("street", "city", "zip_code", "country")}),
        ("Reseaux sociaux", {"fields": ("linkedin", "github", "twitter", "medium")}),
        ("Disponibilite", {"fields": ("availability_status", "availability_message")}),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Administration des soumissions de formulaire de contact."""

    list_display = (
        "name",
        "email",
        "subject",
        "status",
        "formatted_created_at",
        "reference_id",
        "view_message",
    )
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message", "reference_id")
    readonly_fields = (
        "name",
        "email",
        "subject",
        "message",
        "phone",
        "company",
        "ip_address",
        "reference_id",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (None, {"fields": ("name", "email", "subject", "message")}),
        ("Informations complementaires", {"fields": ("phone", "company", "reference_id")}),
        ("Statut et reponse", {"fields": ("status", "response_message", "response_date")}),
        (
            "Donnees techniques",
            {"fields": ("ip_address", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    actions = ["mark_as_responded", "mark_as_closed"]

    @admin.display(description="Date")
    def formatted_created_at(self, obj: Contact) -> str:
        """Formate la date de creation."""
        return obj.created_at.strftime("%d/%m/%Y %H:%M")

    @admin.display(description="Message")
    def view_message(self, obj: Contact) -> SafeString:
        """Affiche un lien pour voir le message complet."""
        return format_html(
            '<a href="{}" target="_blank">Voir</a>',
            reverse("admin:contact_contact_change", args=[obj.pk]),
        )

    @admin.action(description="Marquer comme 'repondu'")
    def mark_as_responded(self, request: HttpRequest, queryset: QuerySet[Contact]) -> None:
        """Marque les soumissions selectionnees comme 'repondu'."""
        count = (
            queryset.exclude(response_message="")
            .exclude(response_message__isnull=True)
            .update(status="responded", response_date=timezone.now())
        )
        self.message_user(request, f"{count} soumission(s) marquee(s) comme 'repondu'.")

    @admin.action(description="Marquer comme 'cloture'")
    def mark_as_closed(self, request: HttpRequest, queryset: QuerySet[Contact]) -> None:
        """Marque les soumissions selectionnees comme 'cloture'."""
        updated = queryset.update(status="closed")
        self.message_user(request, f"{updated} soumission(s) marquee(s) comme 'cloture'.")
