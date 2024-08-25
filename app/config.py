
import os

class Config:
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    PROCESSED_VIDEOS_DIR = "processed_videos/"
    TEMP_DIR = "temp/"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        