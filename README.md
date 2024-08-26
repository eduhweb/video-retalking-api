# VideoReTalking API Project

## Overview

This project is an API built with FastAPI that leverages the VideoReTalking system for audio-based lip synchronization in talking head video editing. The API is designed to process video files by synchronizing lip movements with audio files while allowing for expression customization.

## Features

- **Upload video and audio files**: Submit a video and audio file for processing.
- **Customize expressions**: Choose or define facial expressions for the video.
- **Check job status**: Monitor the processing status of your request.
- **Download results**: Retrieve the processed video after completion.
- **Expiration management**: The results are available for a limited time (15, 30, or 60 minutes).

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python.
- **Celery**: A distributed task queue for handling asynchronous tasks.
- **Redis**: An in-memory data structure store, used as a broker for Celery.
- **Docker**: Containerization of the application for easy deployment.
- **Python**: The primary programming language used in the project.

## Installation

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/video-retalking-api.git
   cd video-retalking-api
   ```

2. Build and run the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This command will start the web server, Redis, and Celery worker.

3. Access the API:

   The API will be available at `http://localhost:8000`.

## API Endpoints

### POST /api/v1/upload

Upload a video and audio file for processing.

**Request Body:**

```json
{
  "video_path": "path/to/video.mp4",
  "audio_path": "path/to/audio.wav",
  "expression_template": "neutral | smile | path/to/custom_expression.jpg",
  "upper_face_expression": "neutral | surprise | angry",
  "result_expiry_minutes": 15 | 30 | 60
}
```

**Response:**

```json
{
  "job_id": "unique_job_identifier",
  "task_id": "celery_task_id",
  "message": "Job started successfully. Use /status/{task_id} to track progress."
}
```

### GET /api/v1/status/{task_id}

Check the status of the processing job.

**Response:**

```json
{
  "status": "pending | processing | completed | failed",
  "result": {
    "download_url": "path/to/output.mp4",
    "expiry_time": "timestamp"
  }
}
```

### GET /api/v1/result/{job_id}

Retrieve the processed video file.

**Response:**

```json
{
  "status": "completed | expired",
  "download_url": "path/to/output.mp4",
  "message": "The result has expired and has been deleted."
}
```

## Development

For development, you can make changes to the source files and restart the Docker containers to see the changes in action.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- **VideoReTalking**: The core technology behind this project.
- **FastAPI**: For providing a fast and easy way to build APIs.
- **Celery**: For managing background tasks efficiently.
- **Redis**: For handling message brokering in Celery.
- **Docker**: For simplifying the deployment process.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs, feature requests, or improvements.