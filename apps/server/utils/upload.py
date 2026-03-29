"""Factory pour les chemins d'upload dynamiques."""

import re
from pathlib import Path

from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


@deconstructible
class UploadTo:
    """Callable serialisable pour les chemins d'upload dynamiques.

    Args:
        prefix: Dossier racine (ex: "articles", "stacks").
        slug_source: Nom du champ (str) ou tuple de champs a concatener.
        fallback: Valeur par defaut si le champ est absent.
    """

    def __init__(
        self,
        prefix: str,
        slug_source: str | tuple[str, ...] = "title",
        fallback: str = "unknown",
    ):
        self.prefix = prefix
        self.slug_source = slug_source
        self.fallback = fallback

    def __call__(self, instance: models.Model, filename: str) -> str:
        if isinstance(self.slug_source, list | tuple):
            parts = [getattr(instance, f, self.fallback) for f in self.slug_source]
            slug = slugify("-".join(parts))
        else:
            slug = slugify(getattr(instance, self.slug_source, self.fallback))

        p = Path(filename)
        safe_base = re.sub(r"[^\w.-]", "_", p.stem)[:100]
        safe_filename = f"{safe_base}{p.suffix.lower()}"
        return f"{self.prefix}/{slug}/{safe_filename}"


def make_upload_to(
    prefix: str,
    slug_source: str | tuple[str, ...] = "title",
    fallback: str = "unknown",
) -> UploadTo:
    """Cree un callable upload_to serialisable par les migrations Django.

    Args:
        prefix: Dossier racine (ex: "articles", "stacks").
        slug_source: Nom du champ (str) ou tuple de champs a concatener.
        fallback: Valeur par defaut si le champ est absent.

    Returns:
        Instance UploadTo compatible avec le parametre upload_to de Django.
    """
    return UploadTo(prefix=prefix, slug_source=slug_source, fallback=fallback)


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
