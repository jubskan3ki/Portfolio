"""Email/SMTP configuration."""

from typing import cast

from config.settings.base import env

# EMAIL

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = cast(str, env("SMTP_HOST"))
EMAIL_PORT = int(str(env("SMTP_PORT")).strip())
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env("SMTP_USER")
EMAIL_HOST_PASSWORD = env("SMTP_PASS")
EMAIL_TIMEOUT = 30
DEFAULT_FROM_EMAIL = env("EMAIL_FROM")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
ADMIN_EMAIL = env("ADMIN_EMAIL")
