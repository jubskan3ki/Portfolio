"""Champs de serialisation personnalises reutilisables."""

import json
from collections.abc import Callable
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from rest_framework import serializers


class JSONBlockListField(serializers.JSONField):
    """JSONField qui valide que la valeur est une liste de blocs JSON.

    Accepte une chaine JSON ou une liste Python. Rejette les non-listes.
    """

    def __init__(
        self,
        *args: Any,
        default: list[Any] | Callable[[], list[Any]] | Any = serializers.empty,
        **kwargs: Any,
    ) -> None:
        # DRF's JSONField stub narrows `default` to Mapping but the field happily accepts lists.
        if default is not serializers.empty:
            kwargs["default"] = default
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: Any) -> list[Any]:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise serializers.ValidationError(f"Format JSON invalide: {e.msg}") from e

        if isinstance(data, list):
            from core.articles.services.article import ArticleService

            return ArticleService.validate_content_blocks(data)

        raise serializers.ValidationError("Le contenu doit etre une chaine JSON ou une liste.")


class URLDictField(serializers.DictField):
    """DictField qui valide que les cles sont dans un ensemble autorise et les valeurs sont des URLs.

    Args:
        allowed_keys: Ensemble de cles autorisees. Si None, toutes les cles sont acceptees.
    """

    def __init__(self, allowed_keys: set[str] | None = None, **kwargs: Any) -> None:
        self.allowed_keys = frozenset(allowed_keys) if allowed_keys else None
        super().__init__(**kwargs)

    def to_internal_value(self, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise serializers.ValidationError("Doit etre un objet JSON.")

        if self.allowed_keys:
            invalid_keys = set(data.keys()) - self.allowed_keys
            if invalid_keys:
                raise serializers.ValidationError(
                    f"Cle(s) non autorisee(s): {', '.join(sorted(invalid_keys))}. "
                    f"Cles acceptees: {', '.join(sorted(self.allowed_keys))}"
                )

        url_validator = URLValidator(schemes=["http", "https"])
        for key, url in data.items():
            if url:
                try:
                    url_validator(url)
                except DjangoValidationError as exc:
                    raise serializers.ValidationError(f"URL invalide pour '{key}': {url}") from exc

        return data
