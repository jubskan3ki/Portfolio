"""Django REST Framework configuration."""

from config.settings.base import DEBUG

REST_FRAMEWORK = {
    # DecimalField -> JSON number (pas string) | évite le wrning Vue prop type.
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.security.jwt_cookie_auth.JWTCookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/minute",
        "user": "1000/day",
        "login": "3/minute",
        "reset_password": "1/minute",
        "change_password": "3/hour",
        "sessions": "30/minute",
        "stack": "10/minute",
        "projects": "10/minute",
        "experience": "10/minute",
        "articles": "10/minute",
        "article_view": "100/minute",
        "project_view": "100/minute",
        "contact": "5/hour",
        "export": "60/hour",
        "import": "30/hour",
        "web_vitals": "180/minute",
        "search": "60/minute",
    },
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.APIResponsePagination",
    "EXCEPTION_HANDLER": "utils.exceptions.handlers.custom_exception_handler",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "utils.renderers.ORJSONRenderer",
        "utils.renderers.ProblemDetailRenderer",
        *(["rest_framework.renderers.BrowsableAPIRenderer"] if DEBUG else []),
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "NUM_PROXIES": 1,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Portfolio API",
    "DESCRIPTION": "API pour le portfolio personnel",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
}
