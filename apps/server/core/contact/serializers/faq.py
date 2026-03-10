"""Serialiseurs pour les FAQs."""

from rest_framework import serializers

from ..models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    """Serialiseur pour les questions frequemment posees."""

    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "is_published", "order"]
        read_only_fields = ["id"]
