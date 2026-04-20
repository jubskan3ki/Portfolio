"""Admin configuration for audit logs."""

from django.contrib import admin
from django.utils.html import escape, format_html
from django.utils.safestring import SafeString

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
        "changes_count",
    ]
    list_filter = ["action", "model_name", "timestamp", "user"]
    search_fields = ["object_id", "object_repr", "user__email", "ip_address", "correlation_id"]
    readonly_fields = [
        "timestamp",
        "action",
        "model_name",
        "object_id",
        "object_repr",
        "changes_pretty",
        "user",
        "ip_address",
        "user_agent",
        "correlation_id",
    ]
    exclude = ["changes"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    def changes_count(self, obj: AuditLog) -> int:
        """Nombre de champs modifies (pour list_display)."""
        return len(obj.changes or {})

    changes_count.short_description = "# fields"

    def changes_pretty(self, obj: AuditLog) -> SafeString:
        """Rend les changements en HTML diff lisible (avant | apres)."""
        if not obj.changes:
            return format_html("<em>Aucun champ modifie.</em>")
        rows = [
            "<table style='border-collapse:collapse;width:100%;font-family:monospace;'>",
            "<tr style='background:#eee;text-align:left;'>"
            "<th style='padding:4px;border:1px solid #ccc;'>Field</th>"
            "<th style='padding:4px;border:1px solid #ccc;'>Before</th>"
            "<th style='padding:4px;border:1px solid #ccc;'>After</th>"
            "</tr>",
        ]
        for field, diff in sorted(obj.changes.items()):
            old = escape(str(diff.get("old")))
            new = escape(str(diff.get("new")))
            rows.append(
                "<tr>"
                f"<td style='padding:4px;border:1px solid #ccc;'><strong>{escape(field)}</strong></td>"
                f"<td style='padding:4px;border:1px solid #ccc;background:#fdecea;'>{old}</td>"
                f"<td style='padding:4px;border:1px solid #ccc;background:#e8f5e9;'>{new}</td>"
                "</tr>"
            )
        rows.append("</table>")
        return format_html("".join(rows))

    changes_pretty.short_description = "Changes (before / after)"

    def has_add_permission(self, _request):
        """Prevent manual creation of audit logs."""
        return False

    def has_change_permission(self, _request, _obj=None):
        """Prevent modification of audit logs."""
        return False

    def has_delete_permission(self, request, _obj=None):
        """Prevent deletion of audit logs (except for superuser)."""
        return request.user.is_superuser
