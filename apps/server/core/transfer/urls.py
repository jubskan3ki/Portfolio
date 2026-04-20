"""URLs pour le module Data Transfer."""

from django.urls import path

from .views import ExportBulkView, ExportDownloadView, ExportModuleView, ImportViewSet, JobViewSet

import_viewset = ImportViewSet.as_view({"post": "import_module"})
import_preview_viewset = ImportViewSet.as_view({"post": "preview"})
import_dry_run_viewset = ImportViewSet.as_view({"post": "dry_run"})
import_bulk_viewset = ImportViewSet.as_view({"post": "bulk_import"})

jobs_list_viewset = JobViewSet.as_view({"get": "list"})
jobs_cleanup_viewset = JobViewSet.as_view({"delete": "cleanup"})
export_job_viewset = JobViewSet.as_view({"get": "export_detail"})
import_job_viewset = JobViewSet.as_view({"get": "import_detail"})

urlpatterns = [
    path("export/module/<str:module>/", ExportModuleView.as_view(), name="export-module"),
    path("export/download/<str:module>/", ExportDownloadView.as_view(), name="export-download"),
    path("export/bulk/", ExportBulkView.as_view(), name="export-bulk"),
    path("import/module/<str:module>/", import_viewset, name="import-module"),
    path("import/preview/<str:module>/", import_preview_viewset, name="import-preview"),
    path("import/dry-run/<str:module>/", import_dry_run_viewset, name="import-dry-run"),
    path("import/bulk/", import_bulk_viewset, name="import-bulk"),
    path("jobs/", jobs_list_viewset, name="jobs-list"),
    path("jobs/cleanup/", jobs_cleanup_viewset, name="jobs-cleanup"),
    path("jobs/export/<uuid:job_id>/", export_job_viewset, name="export-job-detail"),
    path("jobs/import/<uuid:job_id>/", import_job_viewset, name="import-job-detail"),
]
