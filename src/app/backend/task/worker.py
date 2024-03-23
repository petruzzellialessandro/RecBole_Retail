from celery import Celery
import os

BROKER_URI = os.getenv("BROKER_URI", "redis://redis:6379/0")
BACKEND_URI = os.getenv("BACKEND_URI", "redis://redis:6379/0")

app = Celery("celery_task", broker=BROKER_URI, backend=BACKEND_URI, include=["task.tasks"])

app.conf.update(
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    result_backend=BACKEND_URI
)