"""Base strategy interfaces for import/export operations."""

from abc import ABC, abstractmethod
from typing import Any

from django.core.files.uploadedfile import UploadedFile


class ImportStrategy(ABC):
    """Abstract base class for import strategies."""

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return the format name (e.g., 'json', 'csv', 'xlsx')."""

    @property
    @abstractmethod
    def file_extensions(self) -> list[str]:
        """Return supported file extensions."""

    @abstractmethod
    def parse(self, file: UploadedFile) -> list[dict[str, Any]]:
        """
        Parse the uploaded file and return records.

        Args:
            file: Uploaded file object

        Returns:
            List of dictionaries representing records

        Raises:
            ValueError: If file format is invalid
        """

    def can_handle(self, filename: str) -> bool:
        """Check if this strategy can handle the given filename."""
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in self.file_extensions)


class ExportStrategy(ABC):
    """Abstract base class for export strategies."""

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return the format name (e.g., 'json', 'csv', 'xlsx')."""

    @property
    @abstractmethod
    def content_type(self) -> str:
        """Return the MIME content type."""

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Return the file extension (including dot)."""

    @abstractmethod
    def serialize(self, data: list[dict[str, Any]], module: str) -> bytes:
        """
        Serialize data to exportable format.

        Args:
            data: List of dictionaries to export
            module: Module name for context

        Returns:
            Bytes content ready for file write
        """
