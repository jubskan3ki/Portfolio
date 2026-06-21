"""Assainissement des SVG uploades : anti-XSS stocke et anti-XXE.

Un SVG est du XML qui peut embarquer du script ; servi depuis /media/ (meme origine) il
s'executerait dans l'origine de l'app. Nettoyage a l'upload : parsing defusedxml (bloque
XXE/expansion d'entites), suppression des elements/attributs executables, re-serialisation.
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from defusedxml.common import DefusedXmlException
from defusedxml.ElementTree import fromstring as safe_fromstring
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger("security")

_SVG_NS = "http://www.w3.org/2000/svg"
_XLINK_NS = "http://www.w3.org/1999/xlink"

# Elements capables d'executer du script ou d'embarquer du contenu actif.
_BLOCKED_TAGS = {
    "script",
    "foreignobject",
    "iframe",
    "embed",
    "object",
    "handler",
    "audio",
    "video",
    "set",
    "animate",
    "animatemotion",
    "animatetransform",
}

# Attributs portant une URI : seules les images raster en data: sont tolerees.
_URI_ATTR_LOCALNAMES = {"href", "src"}
_SAFE_DATA_PREFIXES = ("data:image/png", "data:image/jpeg", "data:image/gif", "data:image/webp")


def _localname(tag: object) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1].lower()


def _is_dangerous_uri(value: str) -> bool:
    """True si l'URI peut executer du script (javascript:, data: non-raster, vbscript:)."""
    normalized = "".join(value.split()).lower()
    if normalized.startswith(("javascript:", "vbscript:")):
        return True
    if normalized.startswith("data:"):
        return not normalized.startswith(_SAFE_DATA_PREFIXES)
    return False


def _scrub(element: ET.Element) -> None:
    """Supprime recursivement elements et attributs executables."""
    for child in list(element):
        if _localname(child.tag) in _BLOCKED_TAGS:
            element.remove(child)
        else:
            _scrub(child)

    for attr_name, attr_value in list(element.attrib.items()):
        local = _localname(attr_name)
        # on* = gestionnaires d'evenements (onload, onclick...) ; URI = javascript:/data: actif.
        if local.startswith("on") or (local in _URI_ATTR_LOCALNAMES and _is_dangerous_uri(attr_value or "")):
            del element.attrib[attr_name]


def sanitize_svg_bytes(raw: bytes) -> bytes:
    """Parse, nettoie et re-serialise un SVG. Leve ValidationError si invalide."""
    try:
        root = safe_fromstring(raw, forbid_dtd=True)
    except (ET.ParseError, DefusedXmlException, ValueError) as exc:
        raise ValidationError("SVG invalide ou non securise.") from exc

    if _localname(root.tag) != "svg":
        raise ValidationError("Le fichier .svg ne contient pas de SVG valide.")

    _scrub(root)

    ET.register_namespace("", _SVG_NS)
    ET.register_namespace("xlink", _XLINK_NS)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sanitize_svg_upload(image_field) -> bool:
    """Nettoie en place un SVG fraichement uploade (UploadedFile uniquement, persiste via save=False)."""
    if not image_field:
        return False
    try:
        file_obj = image_field.file
    except FileNotFoundError:
        return False
    if not isinstance(file_obj, UploadedFile):
        return False
    if Path(image_field.name).suffix.lower() != ".svg":
        return False

    image_field.seek(0)
    cleaned = sanitize_svg_bytes(image_field.read())
    image_field.save(image_field.name, ContentFile(cleaned), save=False)
    logger.info("SVG assaini a l'upload: %s", image_field.name)
    return True
