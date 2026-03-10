"""URL configuration for portfolio project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

API_PREFIX = "api/"


def health_check(_request):
    """Health check endpoint."""
    return JsonResponse({"status": "ok"})


api_info = openapi.Info(
    title="Portfolio API",
    default_version="v1",
    description="API pour le portfolio personnel",
    terms_of_service="https://www.aitaddajuba.fr/terms/",
    contact=openapi.Contact(email=settings.ADMIN_EMAIL),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    api_info,
    public=settings.DEBUG,
    permission_classes=[permissions.AllowAny if settings.DEBUG else permissions.IsAdminUser],
)

urlpatterns = [
    path("", health_check, name="root"),
    path("admin/", admin.site.urls),
    path(f"{API_PREFIX}users/", include("core.user.urls")),
    path(f"{API_PREFIX}articles/", include("core.articles.urls")),
    path(f"{API_PREFIX}contacts/", include("core.contact.urls")),
    path(f"{API_PREFIX}experiences/", include("core.experiences.urls")),
    path(f"{API_PREFIX}projects/", include("core.projects.urls")),
    path(f"{API_PREFIX}stacks/", include("core.stacks.urls")),
    path(f"{API_PREFIX}transfer/", include("core.transfer.urls")),
    path(f"{API_PREFIX}stats/", include("core.stats.urls")),
    path(f"{API_PREFIX}webhooks/", include("core.webhooks.urls")),
    path(f"{API_PREFIX}audit/", include("core.audit.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("api/schema/", SchemaView.without_ui(cache_timeout=0), name="schema-json"),
        path("swagger/", SchemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
