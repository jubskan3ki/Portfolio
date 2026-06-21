"""Service pour les interactions avec les projets."""

import logging

from django.core.exceptions import ObjectDoesNotExist

from core.stats.models import ViewLog
from utils.exceptions.service import NotFoundError
from utils.services import increment_view_count

from ..models import Project

logger = logging.getLogger("core.projects")


class InteractionService:
    """Service pour les interactions avec les projets (vues)."""

    @staticmethod
    def increment_view_and_get(project_slug: str) -> Project:
        """Incremente le compteur de vues et retourne le projet mis a jour.

        Args:
            project_slug: Slug du projet.

        Returns:
            Le projet mis a jour avec toutes ses relations.

        Raises:
            NotFoundError: Si le projet n'existe pas.
        """
        try:
            project = Project.objects.select_related("category", "status").get(slug=project_slug)
        except ObjectDoesNotExist as exc:
            logger.warning("Projet non trouve pour vue: slug=%s", project_slug)
            raise NotFoundError(
                f"Projet avec le slug '{project_slug}' non trouve.",
                details={"slug": project_slug},
            ) from exc

        increment_view_count(project)
        # increment_view_count fait un UPDATE atomique (F()) sans relire l'objet.
        # On reflete l'increment en memoire au lieu d'un SELECT (refresh_from_db) :
        # le compteur en base reste exact, on economise une requete par vue.
        project.view_count += 1
        ViewLog.objects.log_view("project", project.id)
        return project
