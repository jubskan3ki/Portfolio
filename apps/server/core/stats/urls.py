"""URLs pour le module Stats (Dashboard)."""

from django.urls import path

from .views import (
    DashboardActivityView,
    DashboardChartDataView,
    DashboardOverviewView,
    DashboardQuickStatsView,
    DashboardStatsView,
    WebVitalsIngestView,
    WebVitalsSummaryView,
)

app_name = "stats"

urlpatterns = [
    path("", DashboardStatsView.as_view(), name="stats"),
    path("charts/", DashboardChartDataView.as_view(), name="charts"),
    path("activity/", DashboardActivityView.as_view(), name="activity"),
    path("quick/", DashboardQuickStatsView.as_view(), name="quick"),
    path("overview/", DashboardOverviewView.as_view(), name="overview"),
    path("web-vitals/", WebVitalsIngestView.as_view(), name="web-vitals-ingest"),
    path("web-vitals/summary/", WebVitalsSummaryView.as_view(), name="web-vitals-summary"),
]
