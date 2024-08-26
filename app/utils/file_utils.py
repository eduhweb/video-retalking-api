import os
import time
from app.core.config import settings

def create_result_directory(job_id: str):
    os.makedirs(f"{settings.RESULTS_DIR}/{job_id}", exist_ok=True)

def delete_expired_files(job_id: str):
    result_path = f"{settings.RESULTS_DIR}/{job_id}_output.mp4"
    if os.path.exists(result_path):
        current_time = time.time()
        expiry_time = os.path.getctime(result_path) + settings.result_expiry_minutes * 60
        if current_time > expiry_time:
            os.remove(result_path)
            return {"status": "expired", "message": "The result has expired and has been deleted."}
        return {"status": "completed", "download_url": result_path}
    return {"status": "not found"}
