"""Serializers pour le module Stats (Dashboard)."""

from typing import Any

from rest_framework import serializers

from utils.exceptions.service import ValidationError as ServiceValidationError
from utils.serializers import ReadOnlySerializer

from .services import WebVitalsService


class ModuleStatsSerializer(ReadOnlySerializer):
    """Stats d'un module."""

    count = serializers.IntegerField()
    published = serializers.IntegerField(required=False)
    featured = serializers.IntegerField(required=False)
    new = serializers.IntegerField(required=False)
    responded = serializers.IntegerField(required=False)
    total_views = serializers.IntegerField(required=False)


class DashboardStatsSerializer(ReadOnlySerializer):
    """Serializer pour les statistiques du dashboard."""

    articles = ModuleStatsSerializer()
    projects = ModuleStatsSerializer()
    stacks = ModuleStatsSerializer()
    experiences = ModuleStatsSerializer()
    messages = ModuleStatsSerializer()
    total_views = serializers.IntegerField()


class ViewsDataPointSerializer(ReadOnlySerializer):
    """Point de donnee pour les vues."""

    date = serializers.CharField()
    views = serializers.IntegerField()
    articles_published = serializers.IntegerField(required=False)


class MessagesDataPointSerializer(ReadOnlySerializer):
    """Point de donnee pour les messages."""

    month = serializers.CharField()
    count = serializers.IntegerField()


class ChartDataSerializer(ReadOnlySerializer):
    """Donnees pour les graphiques."""

    views_over_time = ViewsDataPointSerializer(many=True)
    messages_per_month = MessagesDataPointSerializer(many=True)


class ActivityItemSerializer(ReadOnlySerializer):
    """Element d'activite recente."""

    id = serializers.IntegerField()
    type = serializers.CharField()
    action = serializers.CharField()
    title = serializers.CharField()
    timestamp = serializers.DateTimeField()
    module = serializers.CharField()


class RecentActivitySerializer(ReadOnlySerializer):
    """Activite recente."""

    activities = ActivityItemSerializer(many=True)


class QuickStatsSerializer(ReadOnlySerializer):
    """Stats rapides pour le widget."""

    new_messages_today = serializers.IntegerField()
    total_views = serializers.IntegerField()
    popular_article = serializers.CharField(allow_null=True)
    popular_project = serializers.CharField(allow_null=True)


class WebVitalsIngestSerializer(serializers.Serializer):
    """Payload d'ingestion des metriques Web Vitals."""

    name = serializers.ChoiceField(choices=["LCP", "CLS", "INP", "FCP", "TTFB"])
    value = serializers.FloatField()
    rating = serializers.ChoiceField(choices=["good", "needs-improvement", "poor"])
    delta = serializers.FloatField(required=False, default=0)
    id = serializers.CharField(max_length=255)
    page = serializers.CharField(max_length=512)
    url = serializers.CharField(max_length=2048, allow_blank=True, required=False, default="")
    userAgent = serializers.CharField(max_length=1024, allow_blank=True, required=False, default="")
    language = serializers.CharField(max_length=20, allow_blank=True, required=False, allow_null=True)
    viewport = serializers.DictField(required=False, allow_empty=True)
    connectionType = serializers.CharField(max_length=64, allow_blank=True, required=False, allow_null=True)
    isMobile = serializers.BooleanField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False)

    def validate_value(self, value: float) -> float:
        """Delegue la validation au service."""
        try:
            return WebVitalsService.validate_metric_value(value)
        except ServiceValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc

    def validate_delta(self, value: float) -> float:
        """Delegue la validation au service."""
        try:
            return WebVitalsService.validate_metric_delta(value)
        except ServiceValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc

    def validate_viewport(self, value: dict[str, Any]) -> dict[str, Any]:
        """Delegue la normalisation au service."""
        try:
            return WebVitalsService.normalize_viewport(value)
        except ServiceValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc


class WebVitalsSummaryMetricSerializer(ReadOnlySerializer):
    """Resume agrege d'une metrique Web Vitals."""

    metric_name = serializers.CharField()
    count = serializers.IntegerField()
    mean = serializers.FloatField(allow_null=True)
    p75 = serializers.FloatField(allow_null=True)
    p95 = serializers.FloatField(allow_null=True)
    ratings = serializers.DictField(child=serializers.IntegerField())


class WebVitalsSummarySerializer(ReadOnlySerializer):
    """Payload de synthese des Web Vitals."""

    window_days = serializers.IntegerField()
    total_events = serializers.IntegerField()
    metrics = WebVitalsSummaryMetricSerializer(many=True)
