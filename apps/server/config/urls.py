"""Définition des routes principales de l'API Django."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("core.user.urls")),
    path("api/projects/", include("core.projects.urls")),
    path("api/blog/", include("core.blog.urls")),
    path("api/stacks/", include("core.stacks.urls")),
    path("api/contact/", include("core.contact.urls")),
    path("api/experience/", include("core.experience.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
