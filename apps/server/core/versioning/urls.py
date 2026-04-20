"""URLs pour le module versioning."""

from django.urls import path

from .views import TrashListView, UntrashView, VersionListView, VersionRestoreView

app_name = "versioning"

urlpatterns = [
    path("versions/", VersionListView.as_view(), name="versions"),
    path("restore/<int:version_id>/", VersionRestoreView.as_view(), name="restore"),
    path("trashed/", TrashListView.as_view(), name="trashed"),
    path("untrash/", UntrashView.as_view(), name="untrash"),
]
