from app.core.celery_app import celery_app

@celery_app.task
def process_video_task():
    pass  # O processamento real é implementado em app/services/video_processing.py
