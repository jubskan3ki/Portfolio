"""Serializers pour l'export de donnees."""

from rest_framework import serializers

from utils.serializers.base import ReadOnlySerializer

from ..models import ExportJob


class ExportRequestSerializer(ReadOnlySerializer):
    """Serializer pour les requetes d'export."""

    module = serializers.ChoiceField(
        choices=[
            ("articles", "Articles"),
            ("projects", "Projets"),
            ("stacks", "Stacks"),
            ("experiences", "Experiences"),
            ("contacts", "Contacts"),
        ],
        help_text="Module a exporter",
    )
    format = serializers.ChoiceField(
        choices=ExportJob.Format.choices,
        default=ExportJob.Format.JSON,
        help_text="Format d'export",
    )
    filters = serializers.DictField(
        required=False,
        default=dict,
        help_text="Filtres optionnels pour l'export",
    )

    # Cles de pagination/format a exclure des filtres d'export.
    _NON_FILTER_KEYS = frozenset({"export_format", "format", "page", "page_size"})

    @classmethod
    def build_filters(cls, query_params: dict[str, str]) -> dict[str, str]:
        """Extrait les filtres d'export depuis les query params.

        Exclut les cles de pagination et de format qui ne sont pas des filtres.
        """
        return {k: v for k, v in query_params.items() if k not in cls._NON_FILTER_KEYS}


class ExportJobSerializer(serializers.ModelSerializer):
    """Serializer pour les jobs d'export."""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ExportJob
        fields = [
            "id",
            "user_email",
            "module",
            "format",
            "status",
            "filters",
            "records_count",
            "error_message",
            "download_url",
            "created_at",
            "completed_at",
        ]
        read_only_fields = fields

    def get_download_url(self, obj: ExportJob) -> str | None:
        """Retourne l'URL de telechargement si disponible."""
        if obj.file and obj.status == ExportJob.Status.COMPLETED:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
