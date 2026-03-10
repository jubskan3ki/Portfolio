"""Administration des experiences."""

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from .models import Experience, ExperienceType


@admin.register(ExperienceType)
class ExperienceTypeAdmin(admin.ModelAdmin):
    """Admin pour les types d'experiences."""

    list_display = ("name", "experience_count", "icon")
    search_fields = ("name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[ExperienceType]:
        """Optimise les requetes avec Count."""
        return super().get_queryset(request).annotate(_experience_count=Count("experiences"))

    @admin.display(description="Nombre d'experiences")
    def experience_count(self, obj: ExperienceType) -> int:
        """Nombre d'experiences de ce type."""
        return getattr(obj, "_experience_count", 0)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Admin pour les experiences."""

    list_display = ("title", "company", "location", "period", "type", "start_date", "end_date")
    list_filter = ("type", "start_date", "end_date")
    search_fields = ("title", "company", "description")
    list_select_related = ("type",)
    date_hierarchy = "start_date"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "company", "location", "period", "type", "logo")}),
        ("Dates", {"fields": ("start_date", "end_date")}),
        ("Description", {"fields": ("description",)}),
        ("Technologies", {"fields": ("technologies", "achievements")}),
        ("Metadonnees", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
