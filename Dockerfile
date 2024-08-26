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

# Instale PyTorch e torchvision
RUN /bin/bash -c "source activate video_retalking && \
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html"

# Instale as dependências do projeto
RUN /bin/bash -c "source activate video_retalking && \
    pip install -r /app/video-retalking/requirements.txt"

# Etapa 2: Final
FROM python:3.8-alpine

# Instalar ffmpeg na imagem final
RUN apk add --no-cache ffmpeg

# Copie os arquivos necessários da etapa de build
COPY --from=builder /opt/conda/envs/video_retalking /opt/conda/envs/video_retalking
COPY --from=builder /app/video-retalking /app/video-retalking

# Defina o diretório de trabalho
WORKDIR /app

# Defina variáveis de ambiente
ENV PATH=/opt/conda/envs/video_retalking/bin:$PATH

# Instale as dependências da API
RUN pip install fastapi uvicorn celery redis

# Exponha a porta 8000
EXPOSE 8000

# Comando para iniciar o Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
