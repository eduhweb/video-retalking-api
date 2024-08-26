from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "video_retalking",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["worker.tasks"],
)

celery_app.conf.update(task_track_started=True)
