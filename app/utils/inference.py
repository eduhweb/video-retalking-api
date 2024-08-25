
import subprocess
import torch

# Preload model into memory
model = torch.jit.load("path_to_your_model.pt")

def process_video(face_file: str, audio_file: str, output_file: str):
    # Use preloaded model and optimized subprocess call
    subprocess.run([
        "python3", "inference.py",
        "--face", face_file,
        "--audio", audio_file,
        "--outfile", output_file
    ])
            