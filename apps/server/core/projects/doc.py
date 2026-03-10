"""Documentation Swagger centralisee pour le module projects."""

from drf_yasg import openapi

# TAGS

TAGS_PROJECTS = ["Projets"]
TAGS_CATEGORIES = ["Projets - Categories"]
TAGS_STATUSES = ["Projets - Statuts"]
TAGS_STATS = ["Projets - Stats"]

# PARAMETRES COMMUNS

PARAM_PAGE = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="Numero de page",
    type=openapi.TYPE_INTEGER,
    default=1,
    required=False,
)

PARAM_LIMIT = openapi.Parameter(
    "limit",
    openapi.IN_QUERY,
    description="Nombre d'elements par page",
    type=openapi.TYPE_INTEGER,
    default=10,
    required=False,
)

PARAM_CATEGORY = openapi.Parameter(
    "category",
    openapi.IN_QUERY,
    description="Filtrer par categorie (nom ou slug)",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_STATUS = openapi.Parameter(
    "status",
    openapi.IN_QUERY,
    description="Filtrer par statut",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_TECHNOLOGIES = openapi.Parameter(
    "technologies",
    openapi.IN_QUERY,
    description="Filtrer par technologie (peut etre utilise plusieurs fois)",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
    required=False,
)

PARAM_SEARCH = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Recherche textuelle dans le titre, la description et les technologies",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_SORT_BY = openapi.Parameter(
    "sortBy",
    openapi.IN_QUERY,
    description="Champ de tri (date, title, views)",
    type=openapi.TYPE_STRING,
    enum=["date", "title", "views"],
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

PARAM_FEATURED_LIMIT = openapi.Parameter(
    "limit",
    openapi.IN_QUERY,
    description="Nombre de projets a recuperer",
    type=openapi.TYPE_INTEGER,
    default=3,
    required=False,
)

# Liste des parametres pour la liste des projets
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

# SCHEMAS

SCHEMA_PROJECT_LIST_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "slug": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "image": openapi.Schema(type=openapi.TYPE_STRING, format="uri", x_nullable=True),
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "status": openapi.Schema(type=openapi.TYPE_STRING),
        "technologies": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
        ),
        "date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
        "view": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_PAGINATION = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
        "page": openapi.Schema(type=openapi.TYPE_INTEGER),
        "limit": openapi.Schema(type=openapi.TYPE_INTEGER),
        "totalPages": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_PAGINATED_PROJECTS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_PROJECT_LIST_ITEM),
        "pagination": SCHEMA_PAGINATION,
    },
)

SCHEMA_CATEGORY_COUNT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "slug": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_PROJECT_RANKING = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "views": openapi.Schema(type=openapi.TYPE_INTEGER),
        "slug": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_YEAR_COUNT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "year": openapi.Schema(type=openapi.TYPE_INTEGER),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_MONTH_COUNT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "month": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_STATS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "totalProjects": openapi.Schema(type=openapi.TYPE_INTEGER),
        "totalViews": openapi.Schema(type=openapi.TYPE_INTEGER),
        "projectsByCategory": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_CATEGORY_COUNT),
        "mostViewedProjects": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_PROJECT_RANKING),
        "projectsByYear": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_YEAR_COUNT),
        "projectsByMonth": openapi.Schema(type=openapi.TYPE_ARRAY, items=SCHEMA_MONTH_COUNT),
    },
)

# RESPONSES

RESPONSE_200_LIST = openapi.Response(
    description="Liste paginee des projets",
    schema=SCHEMA_PAGINATED_PROJECTS,
)

RESPONSE_200_STATS = openapi.Response(
    description="Statistiques des projets",
    schema=SCHEMA_STATS,
)

RESPONSE_400 = openapi.Response(description="Erreur de validation")
RESPONSE_404 = openapi.Response(description="Ressource non trouvee")
RESPONSE_204 = openapi.Response(description="Suppression reussie")
