# Backend Dockerfile

# Base image for Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
