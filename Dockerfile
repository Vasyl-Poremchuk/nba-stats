FROM python:3.12-slim

WORKDIR /src

# Install system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file & install Python dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI.
RUN pip install --no-cache-dir awscli

# Copy application code.
COPY src/ ./

# Run an entrypoint script.
CMD ["python", "./service.py"]
