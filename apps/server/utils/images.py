"""Optimisation des images a l'upload via Pillow.

Compresse et convertit les images raster en WebP.
Les SVG, GIF et fichiers deja en WebP sont ignores.
"""

import logging
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from PIL import Image

logger = logging.getLogger(__name__)

# Dimensions max selon le type d'image
MAX_SIZE_LARGE = (1920, 1080)  # Articles, projets (images principales)
MAX_SIZE_SMALL = (512, 512)  # Logos, avatars

WEBP_QUALITY = 85
SKIP_EXTENSIONS = {".svg", ".gif", ".webp"}


def optimize_image(image_field, max_size=MAX_SIZE_LARGE, quality=WEBP_QUALITY):
    """Optimise une image : redimensionne et convertit en WebP.

    Ne traite que les nouveaux uploads (UploadedFile).
    Les images deja sauvegardees sur disque (FieldFile) sont ignorees.

    Args:
        image_field: Django ImageField/FileField contenant l'image.
        max_size: Tuple (width, height) max.
        quality: Qualite WebP (1-100).

    Returns:
        True si l'image a ete modifiee, False sinon.
    """
    if not image_field:
        return False

    # Ne traiter que les nouveaux uploads, pas les fichiers deja sauvegardes
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

        # Preserve RGBA for PNG transparency, convert others to RGB
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        # Resize if larger than max dimensions (preserve aspect ratio)
        img.thumbnail(max_size, Image.LANCZOS)

        # Save as WebP
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality, optimize=True)
        buffer.seek(0)

        # Build new filename with .webp extension
        stem = Path(image_field.name).stem
        new_name = f"{stem}.webp"

        image_field.save(new_name, ContentFile(buffer.read()), save=False)
        logger.info("Image optimisee: %s -> %s", image_field.name, new_name)
        return True

    except Exception:
        logger.exception("Erreur lors de l'optimisation de l'image: %s", image_field.name)
        return False
