"""Documentation Swagger centralisee pour le module experiences."""

from drf_yasg import openapi

# TAGS

TAGS_EXPERIENCES = ["Experiences"]
TAGS_TYPES = ["Experiences - Types"]
TAGS_STATS = ["Experiences - Stats"]

# PARAMETRES COMMUNS

PARAM_TYPE = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="Filtrer par type d'experience",
    type=openapi.TYPE_STRING,
    required=False,
)

PARAM_START_YEAR = openapi.Parameter(
    "startYear",
    openapi.IN_QUERY,
    description="Filtrer par annee de debut minimum",
    type=openapi.TYPE_INTEGER,
    required=False,
)

PARAM_END_YEAR = openapi.Parameter(
    "endYear",
    openapi.IN_QUERY,
    description="Filtrer par annee de fin maximum",
    type=openapi.TYPE_INTEGER,
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

EXPERIENCE_LIST_PARAMS = [
    PARAM_TYPE,
    PARAM_START_YEAR,
    PARAM_END_YEAR,
    PARAM_TECHNOLOGIES,
]

# SCHEMAS

SCHEMA_TECHNOLOGY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "level": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_TYPE_COUNT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "type": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "icon": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_STATS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "totalYears": openapi.Schema(type=openapi.TYPE_NUMBER, description="Annees d'experience"),
        "companiesCount": openapi.Schema(type=openapi.TYPE_INTEGER, description="Nombre d'entreprises"),
        "topTechnologies": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=SCHEMA_TECHNOLOGY,
            description="Top technologies",
        ),
        "experienceByType": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=SCHEMA_TYPE_COUNT,
            description="Experiences par type",
        ),
    },
)

SCHEMA_TIMELINE_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "year": openapi.Schema(type=openapi.TYPE_INTEGER),
        "experiences": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
    },
)

SCHEMA_TIMELINE = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=SCHEMA_TIMELINE_ITEM,
)

# RESPONSES

RESPONSE_200_STATS = openapi.Response(description="Statistiques des experiences", schema=SCHEMA_STATS)

RESPONSE_200_TIMELINE = openapi.Response(description="Timeline des experiences", schema=SCHEMA_TIMELINE)

RESPONSE_204 = openapi.Response(description="Supprime avec succes")

RESPONSE_400 = openapi.Response(description="Erreur de validation")

RESPONSE_404 = openapi.Response(description="Ressource non trouvee")
