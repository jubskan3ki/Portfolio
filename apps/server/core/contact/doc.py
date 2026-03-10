"""Documentation Swagger centralisee pour le module contact."""

from drf_yasg import openapi

# TAGS

TAGS_CONTACT = ["Contact"]
TAGS_FAQ = ["Contact - FAQs"]
TAGS_INFO = ["Contact - Info"]
TAGS_STATS = ["Contact - Stats"]

# SCHEMAS

SCHEMA_ADDRESS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "street": openapi.Schema(type=openapi.TYPE_STRING),
        "city": openapi.Schema(type=openapi.TYPE_STRING),
        "zipCode": openapi.Schema(type=openapi.TYPE_STRING),
        "country": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_SOCIAL_MEDIA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "linkedin": openapi.Schema(type=openapi.TYPE_STRING),
        "github": openapi.Schema(type=openapi.TYPE_STRING),
        "twitter": openapi.Schema(type=openapi.TYPE_STRING),
        "medium": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_AVAILABILITY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING),
        "message": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

SCHEMA_POPULAR_SUBJECT = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "subject": openapi.Schema(type=openapi.TYPE_STRING),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

SCHEMA_STATS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "totalMessages": openapi.Schema(type=openapi.TYPE_INTEGER),
        "responseRate": openapi.Schema(type=openapi.TYPE_NUMBER),
        "averageResponseTime": openapi.Schema(type=openapi.TYPE_STRING),
        "popularSubjects": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=SCHEMA_POPULAR_SUBJECT,
        ),
    },
)

SCHEMA_CONTACT_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "message": openapi.Schema(type=openapi.TYPE_STRING),
        "referenceId": openapi.Schema(type=openapi.TYPE_STRING),
        "error_details": openapi.Schema(type=openapi.TYPE_OBJECT),
    },
)

# RESPONSES

RESPONSE_200_STATS = openapi.Response(description="Statistiques de contact", schema=SCHEMA_STATS)

RESPONSE_201_CONTACT = openapi.Response(description="Message envoye", schema=SCHEMA_CONTACT_RESPONSE)

RESPONSE_204 = openapi.Response(description="Supprime avec succes")

RESPONSE_400 = openapi.Response(description="Erreur de validation")

RESPONSE_401 = openapi.Response(description="Non authentifie")

RESPONSE_403 = openapi.Response(description="Permission refusee")

RESPONSE_404 = openapi.Response(description="Ressource non trouvee")

RESPONSE_500 = openapi.Response(description="Erreur serveur")
