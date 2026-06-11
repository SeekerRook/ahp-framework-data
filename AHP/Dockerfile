# Use a lightweight Python image
FROM python:3.8-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY repo/requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=selection.py

# Copy application code
COPY repo/. .

# Expose Flask/Gunicorn port
EXPOSE 8080
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

# Start application with Gunicorn
CMD ["flask","run","-p","8080"]

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]