
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Preload model into memory
RUN python -c "from app.utils.inference import preload_model; preload_model()"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        