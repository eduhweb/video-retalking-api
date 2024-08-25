
from celery import Celery
from .config import Config

celery_app = Celery(
    'video_tasks',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)
celery_app.conf.update(task_track_started=True)
        