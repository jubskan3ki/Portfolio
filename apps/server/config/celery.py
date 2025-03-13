import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("portfolio")

# Tu récupères la conf du settings.py Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover les tasks dans tes apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
