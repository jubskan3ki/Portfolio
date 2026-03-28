"""Documentation centralisee pour le module articles."""

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse

# TAGS

TAGS_ARTICLES = ["Articles"]
TAGS_CATEGORIES = ["Articles - Categories"]
TAGS_TAGS = ["Articles - Tags"]

# PARAMETERS

PARAM_CATEGORY = OpenApiParameter(
    "category",
    location=OpenApiParameter.QUERY,
    description="Filtrer par categorie (nom ou slug)",
    type=str,
    required=False,
)

PARAM_TAG = OpenApiParameter(
    "tag",
    location=OpenApiParameter.QUERY,
    description="Filtrer par tag",
    type=str,
    required=False,
)

PARAM_SEARCH = OpenApiParameter(
    "search",
    location=OpenApiParameter.QUERY,
    description="Recherche textuelle",
    type=str,
    required=False,
)

PARAM_SORT_BY = OpenApiParameter(
    "sortBy",
    location=OpenApiParameter.QUERY,
    description="Champ de tri (date, views, readTime, title)",
    type=str,
    enum=["date", "views", "readTime", "title"],
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

PARAM_LIMIT = OpenApiParameter(
    "limit",
    location=OpenApiParameter.QUERY,
    description="Nombre d'articles a recuperer",
    type=int,
    default=5,
    required=False,
)

PARAM_PAGE = OpenApiParameter(
    "page",
    location=OpenApiParameter.QUERY,
    description="Numero de page",
    type=int,
    default=1,
    required=False,
)

PARAMS_LIST = [PARAM_CATEGORY, PARAM_TAG, PARAM_SEARCH, PARAM_SORT_BY, PARAM_SORT_DIRECTION]
PARAMS_PAGINATION = [PARAM_PAGE, PARAM_LIMIT]

# RESPONSES

RESPONSE_200_ARTICLES = OpenApiResponse(description="Liste paginee des articles")

RESPONSE_200_CATEGORIES = OpenApiResponse(description="Liste des categories")

RESPONSE_200_TAGS = OpenApiResponse(description="Liste des tags")

RESPONSE_204 = OpenApiResponse(description="Supprime avec succes")

RESPONSE_400 = OpenApiResponse(description="Erreur de validation")

RESPONSE_401 = OpenApiResponse(description="Non authentifie")

RESPONSE_403 = OpenApiResponse(description="Permission refusee")

RESPONSE_404 = OpenApiResponse(description="Ressource non trouvee")
