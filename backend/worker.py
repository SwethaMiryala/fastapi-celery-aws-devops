import os
import time

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
TASK_DURATION_SECONDS = int(os.getenv("TASK_DURATION_SECONDS", "10"))

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
    broker_connection_retry_on_startup=True,
)


@celery_app.task(name="send_notification", bind=True)
def send_notification(self, message: str) -> dict:
    """Simulates a slow background job (e.g. sending an email/notification)."""
    time.sleep(TASK_DURATION_SECONDS)
    return {"message": message, "status": "notification sent"}
