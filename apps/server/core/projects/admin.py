"""Administration des projets."""

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from .models import Project, ProjectCategory, ProjectStatus


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """Admin pour les categories de projets."""

    list_display = ("name", "project_count", "description")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request: HttpRequest) -> QuerySet[ProjectCategory]:
        return super().get_queryset(request).annotate(projects_count=Count("projects"))

    @admin.display(description="Projets", ordering="projects_count")
    def project_count(self, obj: ProjectCategory) -> int:
        return getattr(obj, "projects_count", 0)


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    """Admin pour les statuts de projets."""

    list_display = ("name", "project_count", "description")
    search_fields = ("name", "description")

    def get_queryset(self, request: HttpRequest) -> QuerySet[ProjectStatus]:
        return super().get_queryset(request).annotate(projects_count=Count("projects"))

    @admin.display(description="Projets", ordering="projects_count")
    def project_count(self, obj: ProjectStatus) -> int:
        return getattr(obj, "projects_count", 0)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin pour les projets."""

    list_display = ("title", "category", "status", "date", "view_count")
    list_filter = ("category", "status", "date")
    search_fields = ("title", "description", "long_description")
    list_select_related = ("category", "status")
    date_hierarchy = "date"
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("view_count", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "description", "long_description", "image")}),
        ("Categorisation", {"fields": ("category", "status", "technologies", "features")}),
        ("Liens", {"fields": ("links",)}),
        ("Dates", {"fields": ("date", "created_at", "updated_at")}),
        ("Statistiques", {"fields": ("view_count",)}),
    )
