"""Celery configuration for portfolio project."""

import logging
import os

from celery import Celery
from celery.signals import setup_logging, task_failure, worker_ready
from django.db import DatabaseError, connection
from kombu.exceptions import ConnectionError as KombuConnectionError
from kombu.exceptions import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("portfolio")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

logger = logging.getLogger("celery")


@setup_logging.connect
def config_loggers(*_args, **_kwargs):
    import logging.config as logging_config

    try:
        import django

        django.setup()
        from django.conf import settings

        if hasattr(settings, "LOGGING"):
            logging_config.dictConfig(settings.LOGGING)
    except (ImportError, AttributeError, OSError) as e:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s: %(levelname)s/%(name)s] %(message)s",
        )
        logger.warning("Fallback logging: %s", e)


@worker_ready.connect
def worker_ready_handler(sender, **_kwargs):
    try:
        with app.connection() as conn:
            conn.ensure_connection(max_retries=3)
            logger.info("Worker %s connected to broker", sender.hostname)
    except (KombuConnectionError, OperationalError, OSError):
        logger.exception("Worker %s connection error", sender.hostname)


@task_failure.connect
def handle_task_failure(task_id=None, exception=None, **_kwargs):
    # exc_info=exception : le signal s'execute hors bloc except, donc
    # logger.exception() (qui lit sys.exc_info()) ne capturerait pas la trace.
    logger.error("Task %s failed: %s", task_id, exception, exc_info=exception)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    logger.info("Debug task: %r", self.request)
    return f"Debug completed: {self.request.id}"


@app.task(bind=True)
def health_check(self):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except (DatabaseError, OSError) as e:
        # DatabaseError couvre OperationalError/InterfaceError (DB down/injoignable),
        # le cas que ce health check doit precisement signaler sans planter.
        return {"status": "unhealthy", "error": str(e)}
    else:
        return {"status": "healthy", "task_id": self.request.id}
