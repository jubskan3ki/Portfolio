"""Documentation centralisee pour le module projects."""

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse

TAGS_PROJECTS = ["Projets"]
TAGS_CATEGORIES = ["Projets - Categories"]
TAGS_STATUSES = ["Projets - Statuts"]
TAGS_STATS = ["Projets - Stats"]

PARAM_PAGE = OpenApiParameter(
    "page",
    location=OpenApiParameter.QUERY,
    description="Numero de page",
    type=int,
    default=1,
    required=False,
)

PARAM_LIMIT = OpenApiParameter(
    "limit",
    location=OpenApiParameter.QUERY,
    description="Nombre d'elements par page",
    type=int,
    default=10,
    required=False,
)

PARAM_CATEGORY = OpenApiParameter(
    "category",
    location=OpenApiParameter.QUERY,
    description="Filtrer par categorie (nom ou slug)",
    type=str,
    required=False,
)

PARAM_STATUS = OpenApiParameter(
    "status",
    location=OpenApiParameter.QUERY,
    description="Filtrer par statut",
    type=str,
    required=False,
)

PARAM_TECHNOLOGIES = OpenApiParameter(
    "technologies",
    location=OpenApiParameter.QUERY,
    description="Filtrer par technologie (peut etre utilise plusieurs fois)",
    type=str,
    required=False,
)

PARAM_SEARCH = OpenApiParameter(
    "search",
    location=OpenApiParameter.QUERY,
    description="Recherche textuelle dans le titre, la description et les technologies",
    type=str,
    required=False,
)

PARAM_SORT_BY = OpenApiParameter(
    "sortBy",
    location=OpenApiParameter.QUERY,
    description="Champ de tri (date, title, views)",
    type=str,
    enum=["date", "title", "views"],
    default="date",
    required=False,
)

PARAM_SORT_DIRECTION = OpenApiParameter(
    "sortDirection",
    location=OpenApiParameter.QUERY,
    description="Direction du tri (asc, desc)",
    type=str,
    enum=["asc", "desc"],
    default="desc",
    required=False,
)

PARAM_FEATURED_LIMIT = OpenApiParameter(
    "limit",
    location=OpenApiParameter.QUERY,
    description="Nombre de projets a recuperer",
    type=int,
    default=3,
    required=False,
)

PROJECT_LIST_PARAMS = [
    PARAM_CATEGORY,
    PARAM_STATUS,
    PARAM_TECHNOLOGIES,
    PARAM_SEARCH,
    PARAM_SORT_BY,
    PARAM_SORT_DIRECTION,
    PARAM_PAGE,
    PARAM_LIMIT,
]

PAGINATION_PARAMS = [PARAM_PAGE, PARAM_LIMIT]

RESPONSE_200_LIST = OpenApiResponse(description="Liste paginee des projets")

RESPONSE_200_STATS = OpenApiResponse(description="Statistiques des projets")

RESPONSE_400 = OpenApiResponse(description="Erreur de validation")
RESPONSE_404 = OpenApiResponse(description="Ressource non trouvee")
RESPONSE_204 = OpenApiResponse(description="Suppression reussie")
