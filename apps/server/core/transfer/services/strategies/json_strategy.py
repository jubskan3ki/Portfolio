"""JSON import/export strategy."""

import json
from typing import Any

from django.core.files.uploadedfile import UploadedFile

from .base import ExportStrategy, ImportStrategy


class JsonImportStrategy(ImportStrategy):
    """Strategy for importing JSON files."""

    @property
    def format_name(self) -> str:
        return "json"

    @property
    def file_extensions(self) -> list[str]:
        return [".json"]

    def parse(self, file: UploadedFile) -> list[dict[str, Any]]:
        """Parse JSON file."""
        content = file.read().decode("utf-8")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}") from e

        # Handle both flat list and wrapped format
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "data" in data:
            return data["data"]

        raise ValueError("Invalid JSON format. Expected: list or {'data': [...]}")


class JsonExportStrategy(ExportStrategy):
    """Strategy for exporting JSON files."""

    @property
    def format_name(self) -> str:
        return "json"

    @property
    def content_type(self) -> str:
        return "application/json"

    @property
    def file_extension(self) -> str:
        return ".json"

    def serialize(self, data: list[dict[str, Any]], module: str) -> bytes:
        """Serialize data to JSON."""
        output = {
            "module": module,
            "count": len(data),
            "data": data,
        }
        return json.dumps(output, ensure_ascii=False, indent=2, default=str).encode("utf-8")
