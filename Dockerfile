# Step 1: Build Stage
FROM continuumio/miniconda3 AS builder

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    g++ \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone the video-retalking repository
RUN git clone https://github.com/chenxwh/video-retalking.git /app/video-retalking

# Create and activate the Conda environment
RUN conda create -n video_retalking python=3.8 && \
    echo "conda activate video_retalking" >> ~/.bashrc

# Install ffmpeg and other dependencies
RUN conda install -n video_retalking -c conda-forge ffmpeg

# Install PyTorch, Celery, and other dependencies
RUN /bin/bash -c "source activate video_retalking && \
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install -r /app/video-retalking/requirements.txt && \
    pip install fastapi uvicorn celery redis pydantic_settings"

# Step 2: Final Stage
FROM continuumio/miniconda3:latest

COPY --from=builder /opt/conda /opt/conda
COPY --from=builder /app/video-retalking /app/video-retalking

WORKDIR /app

# Set environment variables
ENV PATH=/opt/conda/envs/video_retalking/bin:$PATH
ENV CONDA_DEFAULT_ENV=video_retalking
ENV CONDA_PREFIX=/opt/conda/envs/video_retalking
ENV PATH=$CONDA_PREFIX/bin:$PATH

# Create necessary directories with appropriate permissions
RUN mkdir -p /app/uploads /app/celerybeat-schedule /app/logs

EXPOSE 8000

CMD ["/bin/bash", "-c", "source activate video_retalking && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
