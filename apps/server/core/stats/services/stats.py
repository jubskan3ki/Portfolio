"""Services pour le module Stats (Dashboard)."""

import logging
from datetime import timedelta
from typing import Any

from django.db import models
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from core.articles.models import Article
from core.contact.models import Contact
from core.experiences.models import Experience
from core.projects.models import Project
from core.stacks.models import Stack
from core.stats.models import ViewLog

logger = logging.getLogger("core.stats")

_ACTIVITY_SOURCES: list[dict[str, Any]] = [
    {"model": Article, "type": "article", "module": "articles", "title_field": "title"},
    {"model": Project, "type": "project", "module": "projects", "title_field": "title"},
    {"model": Stack, "type": "stack", "module": "stacks", "title_field": "name"},
    {"model": Experience, "type": "experience", "module": "experiences", "title_field": "title"},
]


class StatsService:
    """Service pour les statistiques du dashboard."""

    @staticmethod
    def get_module_stats() -> dict[str, Any]:
        """Recupere les statistiques de chaque module.

        Optimise avec des requetes agregees pour eviter les N+1.
        """

        articles_agg = Article.objects.aggregate(
            count=Count("id"),
            published=Count("id", filter=Q(is_published=True)),
            featured=Count("id", filter=Q(is_featured=True)),
            total_views=Sum("view_count"),
        )
        articles_stats = {
            "count": articles_agg["count"] or 0,
            "published": articles_agg["published"] or 0,
            "featured": articles_agg["featured"] or 0,
            "total_views": articles_agg["total_views"] or 0,
        }

        projects_agg = Project.objects.aggregate(
            count=Count("id"),
            total_views=Sum("view_count"),
        )
        projects_stats = {
            "count": projects_agg["count"] or 0,
            "total_views": projects_agg["total_views"] or 0,
        }

        stacks_count = Stack.objects.count()
        experiences_count = Experience.objects.count()
        stacks_stats = {"count": stacks_count}
        experiences_stats = {"count": experiences_count}

        messages_agg = Contact.objects.aggregate(
            count=Count("id"),
            new=Count("id", filter=Q(status="new")),
            responded=Count("id", filter=Q(status="responded")),
        )
        messages_stats = {
            "count": messages_agg["count"] or 0,
            "new": messages_agg["new"] or 0,
            "responded": messages_agg["responded"] or 0,
        }

        total_views = articles_stats["total_views"] + projects_stats["total_views"]

        return {
            "articles": articles_stats,
            "projects": projects_stats,
            "stacks": stacks_stats,
            "experiences": experiences_stats,
            "messages": messages_stats,
            "total_views": total_views,
        }

    @staticmethod
    def get_views_over_time(days: int = 30) -> list[dict[str, Any]]:
        """Recupere les vues par jour sur les X derniers jours.

        Utilise le modele ViewLog pour un tracking temporel precis.
        """
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days - 1)

        views_by_date = (
            ViewLog.objects.filter(viewed_at__gte=start_date, viewed_at__lte=end_date)
            .values("viewed_at")
            .annotate(views=Sum("count"))
            .order_by("viewed_at")
        )

        date_data = {item["viewed_at"]: item["views"] for item in views_by_date}

        # Remplit les jours sans events pour obtenir une serie continue (graphiques).
        data = []
        current_date = start_date
        while current_date <= end_date:
            data.append(
                {
                    "date": current_date.isoformat(),
                    "views": date_data.get(current_date, 0),
                }
            )
            current_date += timedelta(days=1)

        return data

    @staticmethod
    def get_messages_per_month(months: int = 6) -> list[dict[str, Any]]:
        """Recupere le nombre de messages par mois."""

        end_date = timezone.now()
        start_date = end_date - timedelta(days=months * 30)

        messages = (
            Contact.objects.filter(created_at__gte=start_date)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        return [
            {
                "month": m["month"].strftime("%Y-%m") if m["month"] else "",
                "count": m["count"],
            }
            for m in messages
        ]

    @staticmethod
    def _collect_model_activities(
        model: type[models.Model], type_name: str, module: str, title_field: str, limit: int
    ) -> list[dict[str, Any]]:
        """Collecte les activites created/updated d'un modele."""
        items = (
            model._default_manager.select_related(None)
            .only("id", title_field, "created_at", "updated_at")
            .order_by("-updated_at")[:limit]
        )
        activities = []
        for item in items:
            created_at = getattr(item, "created_at", None)
            updated_at = getattr(item, "updated_at", None)
            is_new = created_at.date() == updated_at.date() if created_at and updated_at else True
            activities.append(
                {
                    "id": item.pk,
                    "type": type_name,
                    "action": "created" if is_new else "updated",
                    "title": getattr(item, title_field),
                    "timestamp": updated_at,
                    "module": module,
                }
            )
        return activities

    @staticmethod
    def get_recent_activity(limit: int = 10) -> list[dict[str, Any]]:
        """Recupere l'activite recente.

        Combine les activites recentes de plusieurs modules.
        """
        activities: list[dict[str, Any]] = []

        for source in _ACTIVITY_SOURCES:
            activities.extend(
                StatsService._collect_model_activities(
                    model=source["model"],
                    type_name=source["type"],
                    module=source["module"],
                    title_field=source["title_field"],
                    limit=limit,
                )
            )

        # Contact: schema distinct (created_at, titre compose) -> traite separement.
        recent_messages = Contact.objects.only("id", "name", "subject", "created_at").order_by("-created_at")[:limit]
        activities.extend(
            {
                "id": message.id,
                "type": "message",
                "action": "received",
                "title": f"Message de {message.name}: {message.subject}",
                "timestamp": message.created_at,
                "module": "contacts",
            }
            for message in recent_messages
        )

        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:limit]

    @staticmethod
    def get_quick_stats() -> dict[str, Any]:
        """Recupere les stats rapides pour le widget."""

        today = timezone.now().date()

        new_messages_today = Contact.objects.filter(created_at__date=today).count()

        total_article_views = Article.objects.aggregate(total=Sum("view_count"))["total"] or 0
        total_project_views = Project.objects.aggregate(total=Sum("view_count"))["total"] or 0

        popular_article = (
            Article.objects.filter(is_published=True).order_by("-view_count").values_list("title", flat=True).first()
        )

        popular_project = Project.objects.order_by("-view_count").values_list("title", flat=True).first()

        return {
            "new_messages_today": new_messages_today,
            "total_views": total_article_views + total_project_views,
            "popular_article": popular_article,
            "popular_project": popular_project,
        }

    @staticmethod
    def get_chart_data() -> dict[str, Any]:
        """Recupere les donnees pour les graphiques."""
        return {
            "views_over_time": StatsService.get_views_over_time(30),
            "messages_per_month": StatsService.get_messages_per_month(6),
        }

    @staticmethod
    def get_full_dashboard() -> dict[str, Any]:
        """Recupere toutes les donnees du dashboard en une seule methode."""
        return {
            "stats": StatsService.get_module_stats(),
            "charts": StatsService.get_chart_data(),
            "activity": StatsService.get_recent_activity(10),
            "quick_stats": StatsService.get_quick_stats(),
        }
