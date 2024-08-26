from fastapi import FastAPI
from app.api.endpoints import upload

app = FastAPI()

app.include_router(upload.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
