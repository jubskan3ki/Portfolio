"""CSV import/export strategy."""

import csv
import io
import json
from typing import Any

from django.core.files.uploadedfile import UploadedFile

from .base import ExportStrategy, ImportStrategy


class CsvImportStrategy(ImportStrategy):
    """Strategy for importing CSV files."""

    @property
    def format_name(self) -> str:
        return "csv"

    @property
    def file_extensions(self) -> list[str]:
        return [".csv"]

    def parse(self, file: UploadedFile) -> list[dict[str, Any]]:
        """Parse CSV file."""
        content = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        records = []

        for row in reader:
            cleaned_row = self._clean_row(row)
            records.append(cleaned_row)

        return records

    def _clean_row(self, row: dict[str, Any]) -> dict[str, Any]:
        """Clean and parse JSON strings in row values."""
        cleaned: dict[str, Any] = {}
        for key, value in row.items():
            # Note: dict keys from DictReader shouldn't be None in normal operation

            # Try to parse JSON strings back to objects
            if value and isinstance(value, str) and value.startswith(("[", "{")):
                try:
                    cleaned[key] = json.loads(value)
                except json.JSONDecodeError:
                    cleaned[key] = value
            else:
                cleaned[key] = value

        return cleaned


class CsvExportStrategy(ExportStrategy):
    """Strategy for exporting CSV files."""

    @property
    def format_name(self) -> str:
        return "csv"

    @property
    def content_type(self) -> str:
        return "text/csv"

    @property
    def file_extension(self) -> str:
        return ".csv"

    def serialize(self, data: list[dict[str, Any]], _module: str) -> bytes:
        """Serialize data to CSV."""
        if not data:
            return b""

        # Collect all unique keys
        all_keys: set[str] = set()
        for record in data:
            all_keys.update(record.keys())

        fieldnames = sorted(all_keys)

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for record in data:
            # Convert complex objects to JSON strings
            row = {}
            for key in fieldnames:
                value = record.get(key, "")
                if isinstance(value, (list, dict)):
                    row[key] = json.dumps(value, ensure_ascii=False)
                else:
                    row[key] = value
            writer.writerow(row)

        return output.getvalue().encode("utf-8")
