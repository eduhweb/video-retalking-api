
from fastapi import FastAPI
from .routers import video_processing
from .database import SessionLocal

app = FastAPI()

app.include_router(video_processing.router)

@app.on_event("shutdown")
def shutdown_event():
    # Close database connections properly on shutdown
    db = SessionLocal()
    db.close()
        