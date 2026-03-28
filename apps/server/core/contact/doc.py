"""Documentation centralisee pour le module contact."""

from drf_spectacular.utils import OpenApiResponse

# TAGS

TAGS_CONTACT = ["Contact"]
TAGS_FAQ = ["Contact - FAQs"]
TAGS_INFO = ["Contact - Info"]
TAGS_STATS = ["Contact - Stats"]

# RESPONSES

RESPONSE_200_STATS = OpenApiResponse(description="Statistiques de contact")

RESPONSE_201_CONTACT = OpenApiResponse(description="Message envoye")

RESPONSE_204 = OpenApiResponse(description="Supprime avec succes")

RESPONSE_400 = OpenApiResponse(description="Erreur de validation")

RESPONSE_401 = OpenApiResponse(description="Non authentifie")

RESPONSE_403 = OpenApiResponse(description="Permission refusee")

RESPONSE_404 = OpenApiResponse(description="Ressource non trouvee")

RESPONSE_500 = OpenApiResponse(description="Erreur serveur")
