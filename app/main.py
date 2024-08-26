from fastapi import FastAPI
from app.utils.file_utils import setup_logging

app = FastAPI()

# Configuração inicial dos logs
setup_logging()

@app.on_event("startup")
async def startup_event():
    logging.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application shutdown")

# Importa e inclui os roteadores de API
from app.api.endpoints import upload
app.include_router(upload.router, prefix="/api/v1")
