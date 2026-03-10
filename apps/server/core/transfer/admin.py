"""Administration pour le module Data Transfer."""

from django.contrib import admin

from .models import ExportJob, ImportJob


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    """Administration des jobs d'export."""

    list_display = [
        "id",
        "user",
        "module",
        "format",
        "status",
        "records_count",
        "created_at",
        "completed_at",
    ]
    list_filter = ["status", "format", "module", "created_at"]
    search_fields = ["user__email", "module"]
    readonly_fields = [
        "id",
        "user",
        "module",
        "format",
        "status",
        "file",
        "filters",
        "error_message",
        "records_count",
        "created_at",
        "completed_at",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, _request):
        """Desactive l'ajout manuel."""
        return False

    def has_change_permission(self, _request, _obj=None):
        """Desactive la modification."""
        return False


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    """Administration des jobs d'import."""

    list_display = [
        "id",
        "user",
        "module",
        "status",
        "total_records",
        "success_count",
        "error_count",
        "created_at",
        "completed_at",
    ]
    list_filter = ["status", "module", "created_at"]
    search_fields = ["user__email", "module", "original_filename"]
    readonly_fields = [
        "id",
        "user",
        "module",
        "status",
        "original_filename",
        "file_format",
        "total_records",
        "processed_records",
        "success_count",
        "error_count",
        "errors",
        "created_at",
        "completed_at",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, _request):
        """Desactive l'ajout manuel."""
        return False

    def has_change_permission(self, _request, _obj=None):
        """Desactive la modification."""
        return False
