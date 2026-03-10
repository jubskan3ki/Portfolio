"""Administration du module stats."""

from django.contrib import admin
from django.http import HttpRequest

from .models import ViewLog, WebVitalEvent


@admin.register(ViewLog)
class ViewLogAdmin(admin.ModelAdmin):
    """Admin pour les logs de vues."""

    list_display = ("content_type", "content_id", "viewed_at", "count")
    list_filter = ("content_type", "viewed_at")
    search_fields = ("content_type", "content_id")
    ordering = ("-viewed_at",)


@admin.register(WebVitalEvent)
class WebVitalEventAdmin(admin.ModelAdmin):
    """Admin read-only pour les evenements Web Vitals."""

    list_display = ("metric_name", "value", "rating", "path", "created_at")
    list_filter = ("metric_name", "rating", "created_at")
    search_fields = ("path", "metric_id")
    ordering = ("-created_at",)
    readonly_fields = (
        "metric_name",
        "value",
        "rating",
        "delta",
        "metric_id",
        "path",
        "full_url",
        "user_agent",
        "language",
        "viewport_width",
        "viewport_height",
        "connection_type",
        "is_mobile",
        "created_at",
    )

    def has_add_permission(self, _request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, _request: HttpRequest, obj: WebVitalEvent | None = None) -> bool:
        del obj
        return False

    def has_delete_permission(self, _request: HttpRequest, obj: WebVitalEvent | None = None) -> bool:
        del obj
        return False
