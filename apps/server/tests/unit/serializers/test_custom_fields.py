"""Tests unitaires pour les champs de serialisation personnalises."""

from __future__ import annotations

from rest_framework import serializers

from utils.serializers.fields import JSONBlockListField, URLDictField


class JSONBlockListFieldTestSerializer(serializers.Serializer):
    content = JSONBlockListField()


class URLDictFieldTestSerializer(serializers.Serializer):
    links = URLDictField(allowed_keys={"demo", "github", "website"})


class URLDictFieldNoKeysSerializer(serializers.Serializer):
    links = URLDictField()


class TestJSONBlockListField:
    """Tests pour JSONBlockListField."""

    def test_valid_list(self) -> None:
        """Accepte une liste Python avec un bloc paragraph valide."""
        s = JSONBlockListFieldTestSerializer(data={"content": [{"type": "paragraph", "content": "Hello"}]})
        assert s.is_valid(), s.errors
        assert s.validated_data["content"] == [{"type": "paragraph", "content": "Hello"}]

    def test_valid_json_string(self) -> None:
        """Accepte une chaine JSON valide contenant une liste."""
        s = JSONBlockListFieldTestSerializer(data={"content": '[{"type": "heading", "content": "Title", "level": 2}]'})
        assert s.is_valid(), s.errors
        assert s.validated_data["content"] == [{"type": "heading", "content": "Title", "level": 2}]

    def test_empty_list(self) -> None:
        """Accepte une liste vide."""
        s = JSONBlockListFieldTestSerializer(data={"content": []})
        assert s.is_valid(), s.errors
        assert s.validated_data["content"] == []

    def test_invalid_json_string(self) -> None:
        """Rejette une chaine JSON invalide."""
        s = JSONBlockListFieldTestSerializer(data={"content": "{invalid json"})
        assert not s.is_valid()
        assert "content" in s.errors

    def test_json_string_not_list(self) -> None:
        """Rejette une chaine JSON qui n'est pas une liste."""
        s = JSONBlockListFieldTestSerializer(data={"content": '{"key": "value"}'})
        assert not s.is_valid()
        assert "content" in s.errors

    def test_dict_rejected(self) -> None:
        """Rejette un dictionnaire."""
        s = JSONBlockListFieldTestSerializer(data={"content": {"key": "value"}})
        assert not s.is_valid()
        assert "content" in s.errors

    def test_integer_rejected(self) -> None:
        """Rejette un entier."""
        s = JSONBlockListFieldTestSerializer(data={"content": 42})
        assert not s.is_valid()
        assert "content" in s.errors


class TestURLDictField:
    """Tests pour URLDictField."""

    def test_valid_urls(self) -> None:
        """Accepte un dict avec des URLs valides et des cles autorisees."""
        data = {"links": {"demo": "https://example.com", "github": "https://github.com/test"}}
        s = URLDictFieldTestSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_empty_url_value(self) -> None:
        """Accepte une valeur vide (URL optionnelle)."""
        data = {"links": {"demo": "", "github": "https://github.com/test"}}
        s = URLDictFieldTestSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_invalid_key_rejected(self) -> None:
        """Rejette une cle non autorisee."""
        data = {"links": {"unknown_key": "https://example.com"}}
        s = URLDictFieldTestSerializer(data=data)
        assert not s.is_valid()
        assert "links" in s.errors

    def test_invalid_url_rejected(self) -> None:
        """Rejette une URL invalide."""
        data = {"links": {"demo": "not-a-url"}}
        s = URLDictFieldTestSerializer(data=data)
        assert not s.is_valid()
        assert "links" in s.errors

    def test_non_dict_rejected(self) -> None:
        """Rejette un non-dictionnaire."""
        s = URLDictFieldTestSerializer(data={"links": "not-a-dict"})
        assert not s.is_valid()
        assert "links" in s.errors

    def test_list_rejected(self) -> None:
        """Rejette une liste."""
        s = URLDictFieldTestSerializer(data={"links": ["https://example.com"]})
        assert not s.is_valid()
        assert "links" in s.errors

    def test_no_allowed_keys_accepts_any(self) -> None:
        """Sans allowed_keys, accepte n'importe quelle cle."""
        data = {"links": {"any_key": "https://example.com", "another": "https://test.com"}}
        s = URLDictFieldNoKeysSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_empty_dict(self) -> None:
        """Accepte un dictionnaire vide."""
        s = URLDictFieldTestSerializer(data={"links": {}})
        assert s.is_valid(), s.errors
