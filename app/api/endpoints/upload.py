from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from app.services.video_processing import process_video_task
from app.utils.file_utils import create_result_directory, delete_expired_files
from celery.result import AsyncResult

router = APIRouter()

class UploadRequest(BaseModel):
    video_path: str
    audio_path: str
    expression_template: str = "neutral"
    upper_face_expression: str = "neutral"
    result_expiry_minutes: int = 15

@router.post("/upload")
async def upload(request: UploadRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    create_result_directory(job_id)
    task = process_video_task.delay(job_id, request.dict())

    return {"job_id": job_id, "task_id": task.id, "message": "Job started successfully. Use /status/{task_id} to track progress."}

@router.get("/status/{task_id}")
async def status(task_id: str):
    result = AsyncResult(task_id)
    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "STARTED":
        return {"status": "processing"}
    elif result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}
    elif result.state == "FAILURE":
        return {"status": "failed", "message": str(result.result)}
    else:
        return {"status": "unknown"}

@router.get("/result/{job_id}")
async def result(job_id: str):
    return delete_expired_files(job_id)
