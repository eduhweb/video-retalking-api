from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from uuid import uuid4
from app.services.video_processing import process_video_task
from app.utils.file_utils import create_result_directory, delete_expired_files
import os
import shutil

router = APIRouter()

@router.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    video_file: UploadFile = File(...),
    audio_file: UploadFile = File(...),
    expression_template: str = Form("neutral"),
    upper_face_expression: str = Form("neutral"),
    result_expiry_minutes: int = Form(15)
):
    job_id = str(uuid4())
    upload_dir = f"./uploads/{job_id}"
    create_result_directory(upload_dir)

    video_path = f"{upload_dir}/{video_file.filename}"
    audio_path = f"{upload_dir}/{audio_file.filename}"

    try:
        with open(video_path, "wb") as f:
            f.write(await video_file.read())
        with open(audio_path, "wb") as f:
            f.write(await audio_file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save files to disk")

    # Adiciona tarefa de processamento em segundo plano
    background_tasks.add_task(process_video_task, job_id, {
        "video_path": video_path,
        "audio_path": audio_path,
        "expression_template": expression_template,
        "upper_face_expression": upper_face_expression,
        "result_expiry_minutes": result_expiry_minutes
    })

    # Adiciona tarefa de limpeza para rodar depois do tempo de expiração
    background_tasks.add_task(delete_expired_files, upload_dir, result_expiry_minutes)

    return {
        "job_id": job_id,
        "message": "Job started successfully. Use /status/{job_id} to track progress."
    }
