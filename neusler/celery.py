import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neusler.settings.dev")

app = Celery("neusler")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
