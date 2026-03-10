"""Serializers pour l'import de donnees."""

from rest_framework import serializers

from utils.serializers.base import ReadOnlySerializer

from ..models import ImportJob


class ImportRequestSerializer(ReadOnlySerializer):
    """Serializer pour les requetes d'import."""

    module = serializers.ChoiceField(
        choices=[
            ("articles", "Articles"),
            ("projects", "Projets"),
            ("stacks", "Stacks"),
            ("experiences", "Experiences"),
        ],
        help_text="Module cible de l'import",
    )
    file = serializers.FileField(
        help_text="Fichier a importer (JSON, CSV ou XLSX)",
    )
    update_existing = serializers.BooleanField(
        default=False,
        help_text="Mettre a jour les enregistrements existants",
    )


class ImportJobSerializer(serializers.ModelSerializer):
    """Serializer pour les jobs d'import."""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = ImportJob
        fields = [
            "id",
            "user_email",
            "module",
            "status",
            "original_filename",
            "file_format",
            "total_records",
            "processed_records",
            "success_count",
            "error_count",
            "errors",
            "progress",
            "created_at",
            "completed_at",
        ]
        read_only_fields = fields

    def get_progress(self, obj: ImportJob) -> float:
        """Calcule le pourcentage de progression."""
        if obj.total_records == 0:
            return 0.0
        return round((obj.processed_records / obj.total_records) * 100, 2)


class ImportPreviewSerializer(ReadOnlySerializer):
    """Serializer pour la preview d'import."""

    total_records = serializers.IntegerField()
    preview_data = serializers.ListField()
    columns = serializers.ListField(child=serializers.CharField())
    validation_errors = serializers.ListField(default=list)
