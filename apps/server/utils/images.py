"""Compresse et convertit les images raster en WebP. SVG/GIF/WebP ignores."""

import logging
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from PIL import Image

logger = logging.getLogger(__name__)

MAX_SIZE_LARGE = (1920, 1080)  # articles, projets
MAX_SIZE_SMALL = (512, 512)  # logos, avatars

WEBP_QUALITY = 85
SKIP_EXTENSIONS = {".svg", ".gif", ".webp"}


def optimize_image(image_field, max_size=MAX_SIZE_LARGE, quality=WEBP_QUALITY):
    """Redimensionne + convertit en WebP. Traite uniquement les UploadedFile (pas les FieldFile disque)."""
    if not image_field:
        return False

    try:
        file_obj = image_field.file
    except FileNotFoundError:
        return False
    if not isinstance(file_obj, UploadedFile):
        return False

    ext = Path(image_field.name).suffix.lower()
    if ext in SKIP_EXTENSIONS:
        return False

    try:
        image_field.seek(0)
        img = Image.open(image_field)

        # RGBA preserve la transparence PNG, RGB sinon.
        converted = img.convert("RGBA") if img.mode in ("RGBA", "LA", "P") else img.convert("RGB")

        converted.thumbnail(max_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        converted.save(buffer, format="WEBP", quality=quality, optimize=True)
        buffer.seek(0)

        stem = Path(image_field.name).stem
        new_name = f"{stem}.webp"

        image_field.save(new_name, ContentFile(buffer.read()), save=False)
        logger.info("Image optimisee: %s -> %s", image_field.name, new_name)
        return True

    except Exception:
        logger.exception("Erreur lors de l'optimisation de l'image: %s", image_field.name)
        return False
