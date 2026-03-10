"""Documentation Swagger centralisee pour le module Stacks."""

from drf_yasg import openapi

# TAGS

TAGS_STACKS = ["Stacks"]
TAGS_CATEGORIES = ["Stacks - Categories"]
TAGS_RESOURCES = ["Stacks - Ressources"]
TAGS_STATS = ["Stacks - Stats"]

# PARAMETERS COMMUNS

PARAM_CATEGORY = openapi.Parameter(
    "category",
    openapi.IN_QUERY,
    description="Filtrer par categorie",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_TAGS = openapi.Parameter(
    "tags",
    openapi.IN_QUERY,
    description="Filtrer par tags (peut etre utilise plusieurs fois)",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
    required=False,
)

PARAM_MIN_LEVEL = openapi.Parameter(
    "min_level",
    openapi.IN_QUERY,
    description="Niveau de maitrise minimum (0.5-5.0)",
    type=openapi.TYPE_NUMBER,
    required=False,
)

PARAM_MIN_EXPERIENCE = openapi.Parameter(
    "min_experience",
    openapi.IN_QUERY,
    description="Experience minimum en mois",
    type=openapi.TYPE_INTEGER,
    required=False,
)

PARAM_SEARCH = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Recherche textuelle",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_SORT_BY = openapi.Parameter(
    "sort_by",
    openapi.IN_QUERY,
    description="Champ de tri",
    type=openapi.TYPE_STRING,
    enum=["name", "level", "started_date"],
    default="name",
    required=False,
)

PARAM_SORT_DIRECTION = openapi.Parameter(
    "sort_direction",
    openapi.IN_QUERY,
    description="Direction du tri",
    type=openapi.TYPE_STRING,
    enum=["asc", "desc"],
    default="asc",
    required=False,
)

PARAM_STACK_ID = openapi.Parameter(
    "stack_id",
    openapi.IN_QUERY,
    description="ID de la stack pour filtrer",
    type=openapi.TYPE_INTEGER,
    required=False,
)

PARAM_STACK_SLUG = openapi.Parameter(
    "stack_slug",
    openapi.IN_QUERY,
    description="Slug de la stack pour filtrer",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_RESOURCE_TYPE = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="Type de ressource",
    type=openapi.TYPE_STRING,
    enum=["documentation", "tutorial", "article", "video", "other"],
    required=False,
)

# SCHEMAS COMMUNS

SCHEMA_RELATED_STACK = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "logo": openapi.Schema(type=openapi.TYPE_STRING, format="uri", x_nullable=True),
        "slug": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "relationship": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_CATEGORY_COUNT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_STACK_LEVEL = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "level": openapi.Schema(type=openapi.TYPE_NUMBER),
    },
)

SCHEMA_STACK_EXPERIENCE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "years": openapi.Schema(type=openapi.TYPE_NUMBER),
    },
)

SCHEMA_STATS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "totalStacks": openapi.Schema(type=openapi.TYPE_INTEGER),
        "stacksByCategory": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_CATEGORY_COUNT),
        "averageProficiency": openapi.Schema(type=openapi.TYPE_NUMBER),
        "topStacks": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_STACK_LEVEL),
        "yearsOfExperience": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_STACK_EXPERIENCE),
    },
)

# RESPONSES COMMUNES

RESPONSE_400 = openapi.Response(description="Erreur de validation")
RESPONSE_404 = openapi.Response(description="Ressource non trouvee")
RESPONSE_204 = openapi.Response(description="Suppression reussie")

# LISTE DES PARAMETRES PAR ENDPOINT

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
