FROM python:3.13-slim

# Set environment variables
ENV DATABASE_URL=postgresql://bobby:8040@db:5432/jewelry_scraper
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/backend

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the app port
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]
