import os
import shutil
import time
import logging

def create_result_directory(path: str):
    os.makedirs(path, exist_ok=True)

def delete_expired_files(directory: str, delay_minutes: int):
    time.sleep(delay_minutes * 60)  # Espera pelo tempo de expiração
    try:
        shutil.rmtree(directory)  # Deleta o diretório e todo o seu conteúdo
        logging.info(f"Deleted expired directory: {directory}")
    except Exception as e:
        logging.error(f"Failed to delete directory {directory}: {e}")

def setup_logging():
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=f"{log_dir}/app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
