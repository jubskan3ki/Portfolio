"""Constantes centralisees pour le projet portfolio."""

import string

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

MIN_PAGE_LIMIT = 1
MAX_PAGE_LIMIT = 20
DEFAULT_PAGE_LIMIT = 5

DEFAULT_FEATURED_ARTICLES = 5
DEFAULT_POPULAR_ARTICLES = 5
DEFAULT_RELATED_ARTICLES = 3
DEFAULT_FEATURED_PROJECTS = 3
DEFAULT_FEATURED_RESOURCES = 10

MIN_LIMIT = MIN_PAGE_LIMIT
MAX_LIMIT = MAX_PAGE_LIMIT
DEFAULT_LIMIT = DEFAULT_PAGE_LIMIT

ARTICLE_SORT_FIELDS = {
    "date": "published_date",
    "views": "view_count",
    "readTime": "read_time",
    "title": "title",
}

PROJECT_SORT_FIELDS = {
    "date": "date",
    "views": "view_count",
    "title": "title",
    "featured": "is_featured",
}

STACK_SORT_FIELDS = {
    "name": "name",
    "level": "level",
    "order": "order",
}

EXPERIENCE_SORT_FIELDS = {
    "startDate": "start_date",
    "endDate": "end_date",
    "company": "company",
}

QUERY_PARAM_SORT_BY = "sortBy"
QUERY_PARAM_SORT_DIRECTION = "sortDirection"
QUERY_PARAM_LIMIT = "limit"
QUERY_PARAM_PAGE = "page"
QUERY_PARAM_SEARCH = "search"
QUERY_PARAM_CATEGORY = "category"
QUERY_PARAM_TAG = "tag"

DEFAULT_CACHE_TIMEOUT = 600
API_CACHE_TIMEOUT = 600
SESSION_CACHE_TIMEOUT = 86400

DEFAULT_MAX_SESSIONS = 5
DEFAULT_SESSION_TIMEOUT = 24 * 60 * 60
SESSION_CACHE_PREFIX = "user_session"

RESET_CODE_LENGTH = 8
RESET_CODE_CHARS = string.ascii_uppercase + string.digits
RESET_CODE_EXPIRY_MINUTES = 10
RESET_CODE_MAX_ATTEMPTS = 3
MIN_RESPONSE_TIME = 0.5

# Source of truth: config/settings/rest_framework.py
THROTTLE_RATES = {
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
    "contact": "5/hour",
    "export": "60/hour",
    "import": "30/hour",
    "web_vitals": "180/minute",
}

ACCESS_TOKEN_LIFETIME_HOURS = 1
REFRESH_TOKEN_LIFETIME_DAYS = 14

MAX_UPLOAD_SIZE = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "webp"]
ALLOWED_DOCUMENT_EXTENSIONS = ["pdf", "doc", "docx"]

LOG_MAX_BYTES = 10485760
LOG_BACKUP_COUNT = 5

EMAIL_TIMEOUT = 30
EMAIL_MAX_RETRIES = 3
EMAIL_RETRY_DELAY = 60

CACHEABLE_API_URLS = [
    "/api/projects/",
    "/api/experiences/",
    "/api/stacks/",
    "/api/articles/",
]

NON_CACHEABLE_API_URLS = [
    "/api/contact/",
    "/api/admin/",
    "/api/users/",
]

MIN_PASSWORD_LENGTH = 8
MAX_BIO_LENGTH = 1000
MAX_TITLE_LENGTH = 200
MAX_SLUG_LENGTH = 100
