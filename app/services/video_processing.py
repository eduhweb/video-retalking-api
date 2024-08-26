import subprocess
import os
import logging
from celery import Celery
from app.core.config import settings

celery_app = Celery()

@celery_app.task(bind=True)
def process_video_task(self, job_id: str, request: dict):
    try:
        output_file = f"{settings.RESULTS_DIR}/{job_id}_output.mp4"
        command = (
            f"python3 /app/video-retalking/inference.py "
            f"--face {request['video_path']} "
            f"--audio {request['audio_path']} "
            f"--outfile {output_file} "
            f"--exp_img {request['expression_template']} "
            f"--up_face {request['upper_face_expression']}"
        )
        
        # Executa o comando de inferência e captura das saídas
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"Processing completed for job_id {job_id}")
        logging.info(result.stdout)
        if result.stderr:
            logging.warning(result.stderr)

        return {"download_url": output_file, "expiry_time": request["result_expiry_minutes"]}
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed for job_id {job_id} with error: {e.stderr}")
        raise self.retry(exc=e)
