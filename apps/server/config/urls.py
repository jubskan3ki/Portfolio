"""URL configuration for portfolio project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

API_PREFIX = "api/"


def health_check(_request):
    """Health check endpoint."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", health_check, name="root"),
    path("", include("django_prometheus.urls")),
    path("django-admin/", admin.site.urls),
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
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
