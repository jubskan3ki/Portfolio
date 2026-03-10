"""Configuration admin pour le module Stacks."""

from django.contrib import admin
from django.db.models import Count
from django.http import HttpRequest
from django.utils.html import format_html

from .models import RELATIONSHIP_TYPES, Stack, StackCategory, StackRelationship, StackResource


@admin.register(StackCategory)
class StackCategoryAdmin(admin.ModelAdmin):
    """Admin pour les categories de stacks."""

    list_display = ("name", "icon_display", "stack_count", "description_short")
    search_fields = ("name", "description")
    ordering = ("name",)

    def get_queryset(self, request: HttpRequest):
        """Optimise le queryset avec annotation."""
        return super().get_queryset(request).annotate(stacks_count=Count("stacks"))

    @admin.display(description="Stacks", ordering="stacks_count")
    def stack_count(self, obj: StackCategory) -> int:
        """Nombre de stacks (utilise l'annotation)."""
        return getattr(obj, "stacks_count", 0)

    @admin.display(description="Icon")
    def icon_display(self, obj: StackCategory) -> str:
        """Affiche l'icone."""
        return obj.icon or "-"

    @admin.display(description="Description")
    def description_short(self, obj: StackCategory) -> str:
        """Description tronquee."""
        if not obj.description:
            return "-"
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description


class StackResourceInline(admin.TabularInline):
    """Inline pour les ressources de stack."""

    model = StackResource
    extra = 1
    fields = ("title", "type", "url", "is_featured")
    classes = ("collapse",)


class StackRelationshipInline(admin.TabularInline):
    """Inline pour les relations entre stacks."""

    model = StackRelationship
    fk_name = "from_stack"
    extra = 1
    autocomplete_fields = ("to_stack",)
    verbose_name = "Relation"
    verbose_name_plural = "Relations"


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin):
    """Admin pour les stacks techniques."""

    list_display = ("name", "category", "level_display", "experience_display", "resources_count", "updated_at")
    list_filter = ("category", "level")
    search_fields = ("name", "description", "tags")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "experience_calculated")
    inlines = (StackResourceInline, StackRelationshipInline)
    list_select_related = ("category",)
    list_per_page = 25

    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "logo", "category")}),
        ("Competences", {"fields": ("started_date", "experience_calculated", "level", "tags")}),
        (
            "Liens externes",
            {
                "fields": (("website", "website_label"), ("github", "github_label")),
                "classes": ("collapse",),
            },
        ),
        (
            "Informations techniques",
            {
                "fields": ("first_release", "license"),
                "classes": ("collapse",),
            },
        ),
        (
            "Contenu detaille",
            {
                "fields": ("content",),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest):
        """Optimise le queryset avec annotation."""
        return super().get_queryset(request).annotate(res_count=Count("resources"))

    @admin.display(description="Niveau", ordering="level")
    def level_display(self, obj: Stack) -> str:
        """Affiche le niveau avec une barre de progression."""
        percentage = int((float(obj.level) / 5.0) * 100)
        return format_html(
            '<div style="width:100px;background:#ddd;border-radius:4px">'
            '<div style="width:{}%;background:#4CAF50;height:10px;border-radius:4px"></div>'
            "</div> {}",
            percentage,
            obj.level,
        )

    @staticmethod
    def _calculate_experience(started_date) -> tuple[float, int] | None:
        """Calcule l'experience en (annees, mois) depuis la date de debut."""
        if not started_date:
            return None
        from django.utils import timezone

        today = timezone.now().date()
        months = (today.year - started_date.year) * 12 + (today.month - started_date.month)
        return months / 12, months

    @admin.display(description="Experience", ordering="started_date")
    def experience_display(self, obj: Stack) -> str:
        """Affiche l'experience depuis la date de debut."""
        result = self._calculate_experience(obj.started_date)
        if not result:
            return "-"
        years, months = result
        return f"{years:.1f} ans" if years >= 1 else f"{months} mois"

    @admin.display(description="Experience calculee")
    def experience_calculated(self, obj: Stack) -> str:
        """Affiche l'experience calculee en lecture seule."""
        result = self._calculate_experience(obj.started_date)
        if not result:
            return "Aucune date definie"
        years, months = result
        return f"{years:.1f} ans ({months} mois)" if years >= 1 else f"{months} mois"

    @admin.display(description="Ressources", ordering="res_count")
    def resources_count(self, obj: Stack) -> int:
        """Nombre de ressources (utilise l'annotation)."""
        return getattr(obj, "res_count", 0)


@admin.register(StackResource)
class StackResourceAdmin(admin.ModelAdmin):
    """Admin pour les ressources de stacks."""

    list_display = ("title", "stack", "type", "is_featured", "url_link")
    list_filter = ("type", "is_featured", "stack__category")
    search_fields = ("title", "description", "stack__name")
    list_select_related = ("stack",)
    list_per_page = 50

    @admin.display(description="URL")
    def url_link(self, obj: StackResource) -> str:
        """Lien cliquable vers la ressource."""
        return format_html('<a href="{}" target="_blank">Ouvrir</a>', obj.url)


@admin.register(StackRelationship)
class StackRelationshipAdmin(admin.ModelAdmin):
    """Admin pour les relations entre stacks."""

    list_display = ("from_stack", "relationship_display", "to_stack")
    list_filter = ("relationship_type", "from_stack__category", "to_stack__category")
    search_fields = ("from_stack__name", "to_stack__name")
    autocomplete_fields = ("from_stack", "to_stack")
    list_select_related = ("from_stack", "to_stack")

    @admin.display(description="Relation")
    def relationship_display(self, obj: StackRelationship) -> str:
        """Affiche le type de relation avec style."""
        colors = {
            "alternative": "#FF9800",
            "complementary": "#4CAF50",
            "dependency": "#2196F3",
            "similarTo": "#9C27B0",
        }
        color = colors.get(obj.relationship_type, "#757575")
        label = dict(RELATIONSHIP_TYPES).get(obj.relationship_type, obj.relationship_type)
        return format_html('<span style="color:{};font-weight:bold">{}</span>', color, label)
