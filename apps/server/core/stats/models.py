"""Modeles pour le tracking des statistiques."""

import logging

from django.db import models
from django.utils import timezone

from .managers import ViewLogManager, WebVitalEventManager

logger = logging.getLogger("core.stats")


class ViewLog(models.Model):
    """Log des vues pour le tracking temporel."""

    CONTENT_TYPES = [
        ("article", "Article"),
        ("project", "Projet"),
        ("stack", "Stack"),
    ]

    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.PositiveIntegerField()
    viewed_at = models.DateField(default=timezone.now)
    count = models.PositiveIntegerField(default=1)

    objects: ViewLogManager = ViewLogManager()

    class Meta:
        verbose_name = "Log de vue"
        verbose_name_plural = "Logs de vues"
        db_table = "view_logs"
        indexes = [
            models.Index(fields=["viewed_at"]),
            models.Index(fields=["content_type", "content_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "content_id", "viewed_at"],
                name="unique_view_log_per_day",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.content_type}:{self.content_id} - {self.viewed_at} ({self.count})"


class WebVitalEvent(models.Model):
    """Evenement Web Vitals collecte depuis le frontend."""

    class MetricName(models.TextChoices):
        LCP = "LCP", "Largest Contentful Paint"
        CLS = "CLS", "Cumulative Layout Shift"
        INP = "INP", "Interaction to Next Paint"
        FCP = "FCP", "First Contentful Paint"
        TTFB = "TTFB", "Time to First Byte"

    class Rating(models.TextChoices):
        GOOD = "good", "Good"
        NEEDS_IMPROVEMENT = "needs-improvement", "Needs Improvement"
        POOR = "poor", "Poor"

    metric_name = models.CharField(max_length=10, choices=MetricName.choices, db_index=True)
    value = models.FloatField()
    rating = models.CharField(max_length=20, choices=Rating.choices, db_index=True)
    delta = models.FloatField(default=0)
    metric_id = models.CharField(max_length=255, db_index=True)
    path = models.CharField(max_length=512, db_index=True)
    full_url = models.TextField(blank=True)
    user_agent = models.TextField(blank=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    viewport_width = models.PositiveIntegerField(blank=True, null=True)
    viewport_height = models.PositiveIntegerField(blank=True, null=True)
    connection_type = models.CharField(max_length=64, blank=True, null=True)
    is_mobile = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects: WebVitalEventManager = WebVitalEventManager()

    class Meta:
        verbose_name = "Web Vitals Event"
        verbose_name_plural = "Web Vitals Events"
        db_table = "web_vital_events"
        indexes = [
            models.Index(fields=["metric_name", "created_at"]),
            models.Index(fields=["path", "created_at"]),
            models.Index(fields=["rating", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.metric_name} {self.value} ({self.rating}) {self.path}"
