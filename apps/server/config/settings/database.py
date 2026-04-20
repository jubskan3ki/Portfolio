"""Database configuration."""

from config.settings.base import DEBUG, env

# PgBouncer transaction pooling is incompatible with persistent Django connections.
_USE_PGBOUNCER = env.bool("USE_PGBOUNCER", default=False)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "CONN_MAX_AGE": 0 if (_USE_PGBOUNCER or DEBUG) else 60,
        "OPTIONS": {
            "connect_timeout": 10,
            "client_encoding": "UTF8",
            "sslmode": "prefer" if not DEBUG else "disable",
            "application_name": "django-portfolio",
        },
    }
}
