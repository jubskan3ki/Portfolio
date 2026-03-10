"""Documentation Swagger centralisee pour le module articles."""

from drf_yasg import openapi

# TAGS

TAGS_ARTICLES = ["Articles"]
TAGS_CATEGORIES = ["Articles - Categories"]
TAGS_TAGS = ["Articles - Tags"]

# PARAMETERS

PARAM_CATEGORY = openapi.Parameter(
    "category",
    openapi.IN_QUERY,
    description="Filtrer par categorie (nom ou slug)",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_TAG = openapi.Parameter(
    "tag",
    openapi.IN_QUERY,
    description="Filtrer par tag",
    type=openapi.TYPE_STRING,
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
    "sortBy",
    openapi.IN_QUERY,
    description="Champ de tri (date, views, readTime, title)",
    type=openapi.TYPE_STRING,
    enum=["date", "views", "readTime", "title"],
    default="date",
    required=False,
)

PARAM_SORT_DIRECTION = openapi.Parameter(
    "sortDirection",
    openapi.IN_QUERY,
    description="Direction du tri (asc, desc)",
    type=openapi.TYPE_STRING,
    enum=["asc", "desc"],
    default="desc",
    required=False,
)

PARAM_LIMIT = openapi.Parameter(
    "limit",
    openapi.IN_QUERY,
    description="Nombre d'articles a recuperer",
    type=openapi.TYPE_INTEGER,
    default=5,
    required=False,
)

PARAM_PAGE = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="Numero de page",
    type=openapi.TYPE_INTEGER,
    default=1,
    required=False,
)

PARAMS_LIST = [PARAM_CATEGORY, PARAM_TAG, PARAM_SEARCH, PARAM_SORT_BY, PARAM_SORT_DIRECTION]
PARAMS_PAGINATION = [PARAM_PAGE, PARAM_LIMIT]

# SCHEMAS

SCHEMA_PAGINATION = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
        "page": openapi.Schema(type=openapi.TYPE_INTEGER),
        "limit": openapi.Schema(type=openapi.TYPE_INTEGER),
        "totalPages": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_ARTICLE_LIST = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "slug": openapi.Schema(type=openapi.TYPE_STRING),
        "excerpt": openapi.Schema(type=openapi.TYPE_STRING),
        "image": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "tags": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
        "date": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
        "readTime": openapi.Schema(type=openapi.TYPE_INTEGER),
        "views": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_ARTICLE_PAGINATED = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_ARTICLE_LIST),
        "pagination": SCHEMA_PAGINATION,
    },
)

SCHEMA_CATEGORY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "slug": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_TAG = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

# RESPONSES

RESPONSE_200_ARTICLES = openapi.Response(
    description="Liste paginee des articles",
    schema=SCHEMA_ARTICLE_PAGINATED,
)

RESPONSE_200_CATEGORIES = openapi.Response(
    description="Liste des categories",
    schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_CATEGORY),
)

RESPONSE_200_TAGS = openapi.Response(
    description="Liste des tags",
    schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_TAG),
)

RESPONSE_204 = openapi.Response(description="Supprime avec succes")

RESPONSE_400 = openapi.Response(description="Erreur de validation")

RESPONSE_401 = openapi.Response(description="Non authentifie")

RESPONSE_403 = openapi.Response(description="Permission refusee")

RESPONSE_404 = openapi.Response(description="Ressource non trouvee")
