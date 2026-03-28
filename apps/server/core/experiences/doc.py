"""Documentation centralisee pour le module experiences."""

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse

# TAGS

TAGS_EXPERIENCES = ["Experiences"]
TAGS_TYPES = ["Experiences - Types"]
TAGS_STATS = ["Experiences - Stats"]

# PARAMETRES COMMUNS

PARAM_TYPE = OpenApiParameter(
    "type",
    location=OpenApiParameter.QUERY,
    description="Filtrer par type d'experience",
    type=str,
    required=False,
)

PARAM_START_YEAR = OpenApiParameter(
    "startYear",
    location=OpenApiParameter.QUERY,
    description="Filtrer par annee de debut minimum",
    type=int,
    required=False,
)

PARAM_END_YEAR = OpenApiParameter(
    "endYear",
    location=OpenApiParameter.QUERY,
    description="Filtrer par annee de fin maximum",
    type=int,
    required=False,
)

PARAM_TECHNOLOGIES = OpenApiParameter(
    "technologies",
    location=OpenApiParameter.QUERY,
    description="Filtrer par technologie (peut etre utilise plusieurs fois)",
    type=str,
    required=False,
)

EXPERIENCE_LIST_PARAMS = [
    PARAM_TYPE,
    PARAM_START_YEAR,
    PARAM_END_YEAR,
    PARAM_TECHNOLOGIES,
]

# RESPONSES

RESPONSE_200_STATS = OpenApiResponse(description="Statistiques des experiences")

RESPONSE_200_TIMELINE = OpenApiResponse(description="Timeline des experiences")

RESPONSE_204 = OpenApiResponse(description="Supprime avec succes")

RESPONSE_400 = OpenApiResponse(description="Erreur de validation")

RESPONSE_404 = OpenApiResponse(description="Ressource non trouvee")
