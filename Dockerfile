FROM continuumio/miniconda3

WORKDIR /app

COPY . /app

RUN git clone https://github.com/chenxwh/video-retalking.git /app/video-retalking

RUN conda create -n video_retalking python=3.8 && \
    echo "conda activate video_retalking" >> ~/.bashrc

RUN conda install -n video_retalking -c conda-forge ffmpeg

RUN /bin/bash -c "source activate video_retalking && \
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html"

RUN /bin/bash -c "source activate video_retalking && \
    pip install -r /app/video-retalking/requirements.txt"

RUN /bin/bash -c "source activate video_retalking && \
    pip install fastapi uvicorn celery redis"

EXPOSE 8000

CMD ["/bin/bash", "-c", "source activate video_retalking && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
