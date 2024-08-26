import os
import subprocess
from app.core.config import settings
from worker.tasks import celery_app

@celery_app.task(bind=True)
def process_video_task(self, job_id: str, request: dict):
    try:
        output_file = f"{settings.RESULTS_DIR}/{job_id}_output.mp4"
        command = (
            f"python3 video-retalking/inference.py "
            f"--face {request['video_path']} "
            f"--audio {request['audio_path']} "
            f"--outfile {output_file} "
            f"--exp_img {request['expression_template']} "
            f"--up_face {request['upper_face_expression']}"
        )
        
        # Execução do comando de inferência
        subprocess.run(command, shell=True, check=True)
        
        return {"download_url": output_file, "expiry_time": request["result_expiry_minutes"]}
    except subprocess.CalledProcessError as e:
        raise self.retry(exc=e)
