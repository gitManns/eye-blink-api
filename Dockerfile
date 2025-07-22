# Use official Python image with specific version
FROM python:3.10-slim

# Install system dependencies required by mediapipe
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port (match your FastAPI uvicorn port)
EXPOSE 10000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]