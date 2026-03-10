"""Serialiseurs pour les statistiques de contact."""

from rest_framework import serializers

from utils.serializers.base import ReadOnlySerializer


class ContactStatsSerializer(ReadOnlySerializer):
    """Serialiseur pour les statistiques de contact."""

    totalMessages = serializers.IntegerField()
    responseRate = serializers.FloatField()
    averageResponseTime = serializers.CharField()
    popularSubjects = serializers.ListField(child=serializers.DictField())
