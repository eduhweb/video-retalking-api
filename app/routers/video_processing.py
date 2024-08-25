
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from starlette.responses import FileResponse
from celery.result import AsyncResult
from ..workers.worker import process_video_task
from ..config import Config
from ..database import SessionLocal, ProcessedFile
import os
import shutil

router = APIRouter()

def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        db = SessionLocal()
        db.query(ProcessedFile).filter(ProcessedFile.file_path == file_path).delete()
        db.commit()

@router.post("/process-video/")
async def process_video(face: UploadFile = File(...), audio: UploadFile = File(...), background_tasks: BackgroundTasks):
    face_path = os.path.join(Config.TEMP_DIR, face.filename)
    audio_path = os.path.join(Config.TEMP_DIR, audio.filename)
    
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    with open(face_path, "wb") as f:
        shutil.copyfileobj(face.file, f)
        
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)
    
    task = process_video_task.delay(face_path, audio_path)

    # Schedule deletion of temp files after 15 minutes
    background_tasks.add_task(delete_file, face_path)
    background_tasks.add_task(delete_file, audio_path)

    return {"task_id": task.id}

@router.get("/download/{task_id}")
async def download_video(task_id: str, background_tasks: BackgroundTasks):
    task_result = AsyncResult(task_id)
    
    if task_result.state != "SUCCESS":
        raise HTTPException(status_code=400, detail="Video processing not completed")
    
    file_path = task_result.result
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(path=file_path, filename=os.path.basename(file_path))

    # Schedule deletion of processed video file after 15 minutes
    background_tasks.add_task(delete_file, file_path)

    return response
            