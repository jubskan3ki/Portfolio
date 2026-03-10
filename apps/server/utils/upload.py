"""Factory pour les chemins d'upload dynamiques."""

import os
import re

from django.db import models
from django.utils.text import slugify


def make_upload_to(
    prefix: str,
    slug_source: str | tuple[str, ...] = "title",
    fallback: str = "unknown",
):
    """Cree une fonction upload_to dynamique basee sur un champ du modele.

    Args:
        prefix: Dossier racine (ex: "articles", "stacks").
        slug_source: Nom du champ (str) ou tuple de champs a concatener.
        fallback: Valeur par defaut si le champ est absent.

    Returns:
        Callable compatible avec le parametre upload_to de Django.
    """

    def upload_to(instance: models.Model, filename: str) -> str:
        if isinstance(slug_source, (list, tuple)):
            parts = [getattr(instance, f, fallback) for f in slug_source]
            slug = slugify("-".join(parts))
        else:
            slug = slugify(getattr(instance, slug_source, fallback))

        # Sanitize filename: keep only the last extension, slugify the base name
        base, ext = os.path.splitext(filename)
        safe_base = re.sub(r"[^\w.-]", "_", base)[:100]
        safe_filename = f"{safe_base}{ext.lower()}"
        return f"{prefix}/{slug}/{safe_filename}"

    return upload_to


def extract_images_from_files(files) -> dict:
    """Extrait les images d'un MultiValueDict avec le pattern images[key].

    Args:
        files: MultiValueDict de fichiers uploades (request.FILES).

    Returns:
        Dict {key: file} pour chaque fichier correspondant au pattern.
    """
    images: dict = {}
    for key in files:
        if key.startswith("images[") and key.endswith("]"):
            image_key = key[7:-1]
            images[image_key] = files.get(key)
    return images
