# Video Processing API

## Description

The Video Processing API is a web application based on FastAPI that allows you to process videos using audio and video files. It provides endpoints to upload videos and audio, track the progress of the processing, and download the processed video. The project uses Celery for managing asynchronous tasks and Docker for containerization, ensuring that the application is scalable and easy to deploy.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Docker Installation](#docker-installation)
  - [Local Installation](#local-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, make sure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## Installation

### Docker Installation

The easiest way to set up and run the application is by using Docker and Docker Compose.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/eduhweb/video-processing-api.git
   cd video-processing-api
   ```

2. **Build and start the containers:**

   Run the command below to build the Docker images and start the containers:

   ```bash
   docker-compose up --build
   ```

   This will start the following services:
   - `api`: The FastAPI application, accessible at `http://localhost:8000`.
   - `worker`: The Celery worker that processes the videos.
   - `redis`: The in-memory database used as a broker by Celery.

3. **Access the application:**

   Open your browser and go to `http://localhost:8000/docs` to view the interactive API documentation.

### Local Installation

If you prefer to run the application locally without Docker, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/eduhweb/video-processing-api.git
   cd video-processing-api
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis:**

   Make sure Redis is installed and running on your local machine. If you're using Docker, you can start Redis with:

   ```bash
   docker run -d -p 6379:6379 redis
   ```

5. **Start Celery:**

   In a new terminal window, start the Celery worker:

   ```bash
   celery -A app.celery_config.celery_app worker --loglevel=info
   ```

6. **Start the FastAPI server:**

   Run the FastAPI server:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

   The application will be available at `http://localhost:8000`.

## Usage

After installation, you can use the API to process videos. Access the interactive API documentation at `http://localhost:8000/docs` to explore the endpoints and test the functionalities.

## API Endpoints

Here are the main endpoints available in the API:

- **POST /process-video/**

  Upload a video and an audio file to start the processing. Returns a `task_id` that can be used to track the progress.

  **Request example:**

  ```
  curl -X POST "http://localhost:8000/process-video/" -F "face=@path/to/video.mp4" -F "audio=@path/to/audio.wav"
  ```

- **GET /progress/{task_id}**

  Check the status of the video processing. Returns the task state and, if completed, the path to the processed video.

  **Request example:**

  ```
  curl -X GET "http://localhost:8000/progress/{task_id}"
  ```

- **GET /download/{task_id}**

  Download the processed video and get the remaining time before the file is automatically deleted.

  **Request example:**

  ```
  curl -X GET "http://localhost:8000/download/{task_id}"
  ```

## Contributing

Contributions are welcome! If you want to help improve this project, follow these steps:

1. **Fork the repository.**
2. **Create a new branch for your feature (`git checkout -b feature/new-feature`).**
3. **Commit your changes (`git commit -am 'Add new feature'`).**
4. **Push to the branch (`git push origin feature/new-feature`).**
5. **Open a Pull Request.**

## License

This project is licensed under the terms of the MIT license. See the `LICENSE` file for more details.