from pydantic import BaseSettings

class Settings(BaseSettings):
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    RESULTS_DIR: str = "./results"
    CHECKPOINTS_DIR: str = "./checkpoints"

settings = Settings()
