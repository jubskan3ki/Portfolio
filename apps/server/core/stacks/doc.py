"""Documentation centralisee pour le module Stacks."""

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse

TAGS_STACKS = ["Stacks"]
TAGS_CATEGORIES = ["Stacks - Categories"]
TAGS_RESOURCES = ["Stacks - Ressources"]
TAGS_STATS = ["Stacks - Stats"]

PARAM_CATEGORY = OpenApiParameter(
    "category",
    location=OpenApiParameter.QUERY,
    description="Filtrer par categorie",
    type=str,
    required=False,
)

PARAM_TAGS = OpenApiParameter(
    "tags",
    location=OpenApiParameter.QUERY,
    description="Filtrer par tags (peut etre utilise plusieurs fois)",
    type=str,
    required=False,
)

PARAM_MIN_LEVEL = OpenApiParameter(
    "min_level",
    location=OpenApiParameter.QUERY,
    description="Niveau de maitrise minimum (0.5-5.0)",
    type=float,
    required=False,
)

PARAM_MIN_EXPERIENCE = OpenApiParameter(
    "min_experience",
    location=OpenApiParameter.QUERY,
    description="Experience minimum en mois",
    type=int,
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
    "sort_by",
    location=OpenApiParameter.QUERY,
    description="Champ de tri",
    type=str,
    enum=["name", "level", "started_date"],
    default="name",
    required=False,
)

PARAM_SORT_DIRECTION = OpenApiParameter(
    "sort_direction",
    location=OpenApiParameter.QUERY,
    description="Direction du tri",
    type=str,
    enum=["asc", "desc"],
    default="asc",
    required=False,
)

PARAM_STACK_ID = OpenApiParameter(
    "stack_id",
    location=OpenApiParameter.QUERY,
    description="ID de la stack pour filtrer",
    type=int,
    required=False,
)

PARAM_STACK_SLUG = OpenApiParameter(
    "stack_slug",
    location=OpenApiParameter.QUERY,
    description="Slug de la stack pour filtrer",
    type=str,
    required=False,
)

PARAM_RESOURCE_TYPE = OpenApiParameter(
    "type",
    location=OpenApiParameter.QUERY,
    description="Type de ressource",
    type=str,
    enum=["documentation", "tutorial", "article", "video", "other"],
    required=False,
)

RESPONSE_200_STATS = OpenApiResponse(description="Statistiques des stacks")
RESPONSE_400 = OpenApiResponse(description="Erreur de validation")
RESPONSE_404 = OpenApiResponse(description="Ressource non trouvee")
RESPONSE_204 = OpenApiResponse(description="Suppression reussie")

STACK_LIST_PARAMS = [
    PARAM_CATEGORY,
    PARAM_TAGS,
    PARAM_MIN_LEVEL,
    PARAM_MIN_EXPERIENCE,
    PARAM_SEARCH,
    PARAM_SORT_BY,
    PARAM_SORT_DIRECTION,
]

RESOURCE_LIST_PARAMS = [
    PARAM_STACK_ID,
    PARAM_STACK_SLUG,
    PARAM_RESOURCE_TYPE,
]
