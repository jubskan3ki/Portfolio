"""Admin configuration for audit logs."""

from django.contrib import admin

from core.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for viewing audit logs."""

    list_display = [
        "timestamp",
        "action",
        "model_name",
        "object_id",
        "user",
        "ip_address",
    ]
    list_filter = ["action", "model_name", "timestamp"]
    search_fields = ["object_id", "object_repr", "user__email", "ip_address"]
    readonly_fields = [
        "timestamp",
        "action",
        "model_name",
        "object_id",
        "object_repr",
        "changes",
        "user",
        "ip_address",
        "user_agent",
        "correlation_id",
    ]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    def has_add_permission(self, _request):
        """Prevent manual creation of audit logs."""
        return False

    def has_change_permission(self, _request, _obj=None):
        """Prevent modification of audit logs."""
        return False

    def has_delete_permission(self, request, _obj=None):
        """Prevent deletion of audit logs (except for superuser)."""
        return request.user.is_superuser
