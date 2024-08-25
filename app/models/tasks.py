
from celery import shared_task
from ..utils.inference import process_video
from ..database import SessionLocal, ProcessedFile
from ..config import Config
import os

@shared_task
def process_video_task(face_file: str, audio_file: str):
    output_file = f"{face_file.split('/')[-1].split('.')[0]}_output.mp4"
    output_path = os.path.join(Config.PROCESSED_VIDEOS_DIR, output_file)
    
    process_video(face_file, audio_file, output_path)
    
    db = SessionLocal()
    db.add(ProcessedFile(file_path=output_path))
    db.commit()
    
    # Schedule deletion of the processed video file after 15 minutes
    delete_file_after_delay.apply_async(args=[output_path], countdown=15*60)
    
    return output_path

@shared_task
def delete_file_after_delay(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        db = SessionLocal()
        db.query(ProcessedFile).filter(ProcessedFile.file_path == file_path).delete()
        db.commit()
            