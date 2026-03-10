"""Vues pour le module projects."""

from .category import CategoryViewSet
from .project import ProjectViewSet
from .stats import StatsView
from .status import StatusViewSet

__all__ = [
    "CategoryViewSet",
    "ProjectViewSet",
    "StatsView",
    "StatusViewSet",
]
