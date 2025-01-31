# Use the Python base image
FROM python:3.9-slim-bullseye

# Set the working directory
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Install system dependencies for MySQL support and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    gnupg \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/logs

# Copy the backend code
COPY python-server .

# Expose the backend port
EXPOSE 3000

# Start the Python server
CMD ["python", "server.py"]
