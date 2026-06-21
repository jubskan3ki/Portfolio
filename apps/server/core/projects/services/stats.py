"""Service pour les statistiques des projets."""

import logging
from typing import TypedDict

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone

from ..models import Project, ProjectCategory

logger = logging.getLogger("core.projects")


class CategoryCount(TypedDict):
    """Type pour le comptage par categorie."""

    category: str
    count: int
    slug: str


class ProjectRanking(TypedDict):
    """Type pour le classement de projets."""

    title: str
    views: int
    slug: str
    category: str


class YearCount(TypedDict):
    """Type pour le comptage par annee."""

    year: int
    count: int


class MonthCount(TypedDict):
    """Type pour le comptage par mois."""

    month: str
    count: int


class ProjectStats(TypedDict):
    """Type pour les statistiques des projets."""

    totalProjects: int
    totalViews: int
    projectsByCategory: list[CategoryCount]
    mostViewedProjects: list[ProjectRanking]
    projectsByYear: list[YearCount]
    projectsByMonth: list[MonthCount]


class StatsService:
    """Service pour les statistiques des projets."""

    @staticmethod
    def get_stats() -> ProjectStats:
        """Calcule les statistiques globales des projets.

        Returns:
            Dictionnaire contenant les statistiques.
        """
        aggregates = Project.objects.aggregate(
            total=Count("id"),
            views=Sum("view_count"),
        )

        total_projects = aggregates["total"] or 0
        total_views = aggregates["views"] or 0

        projects_by_category = ProjectCategory.objects.annotate(count=Count("projects")).values("name", "count", "slug")

        most_viewed = Project.objects.order_by("-view_count")[:5].values(
            "title", "view_count", "slug", "category__name"
        )

        projects_by_year = (
            Project.objects.annotate(year=TruncYear("date")).values("year").annotate(count=Count("id")).order_by("year")
        )

        current_year = timezone.now().year
        last_year = current_year - 1

        projects_by_month = (
            Project.objects.filter(date__year__gte=last_year)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        return {
            "totalProjects": total_projects,
            "totalViews": total_views,
            "projectsByCategory": [
                {"category": item["name"], "count": item["count"], "slug": item["slug"]}
                for item in projects_by_category
            ],
            "mostViewedProjects": [
                {
                    "title": item["title"],
                    "views": item["view_count"],
                    "slug": item["slug"],
                    "category": item["category__name"] or "",
                }
                for item in most_viewed
            ],
            "projectsByYear": [
                {"year": item["year"].year, "count": item["count"]} for item in projects_by_year if item["year"]
            ],
            "projectsByMonth": [
                {"month": item["month"].strftime("%Y-%m"), "count": item["count"]}
                for item in projects_by_month
                if item["month"]
            ],
        }
