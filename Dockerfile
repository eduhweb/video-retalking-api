# Etapa 1: Build
FROM continuumio/miniconda3 AS builder

# Defina o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    g++ \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone o repositório video-retalking
RUN git clone https://github.com/chenxwh/video-retalking.git /app/video-retalking

# Crie e ative o ambiente Conda
RUN conda create -n video_retalking python=3.8 && \
    echo "conda activate video_retalking" >> ~/.bashrc

# Instale ffmpeg e dependências
RUN conda install -n video_retalking -c conda-forge ffmpeg

# Instale PyTorch, Celery e outras dependências
RUN /bin/bash -c "source activate video_retalking && \
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install -r /app/video-retalking/requirements.txt && \
    pip install fastapi uvicorn celery redis pydantic_settings"

# Etapa 2: Final
FROM continuumio/miniconda3:latest

# Criar usuário não privilegiado
RUN useradd -m -s /bin/bash celeryuser

# Copie o ambiente Conda completo da etapa de build
COPY --from=builder /opt/conda /opt/conda
COPY --from=builder /app/video-retalking /app/video-retalking

# Defina o diretório de trabalho
WORKDIR /app

# Defina variáveis de ambiente
ENV PATH=/opt/conda/envs/video_retalking/bin:$PATH
ENV CONDA_DEFAULT_ENV=video_retalking
ENV CONDA_PREFIX=/opt/conda/envs/video_retalking
ENV PATH=$CONDA_PREFIX/bin:$PATH

# Mude para o usuário não privilegiado
USER celeryuser

# Exponha a porta 8000
EXPOSE 8000

# Comando para iniciar o Uvicorn
CMD ["/bin/bash", "-c", "source activate video_retalking && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
