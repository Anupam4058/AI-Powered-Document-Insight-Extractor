# Backend - AI Document Insight Extractor
# Optimized for AWS EC2 t2.micro (1GB RAM) – CPU-only, slim image
FROM python:3.11-slim-bookworm

# Runtime deps for PyTorch CPU and pdf/docx (minimal for smaller image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code (tests/dev files excluded via .dockerignore)
COPY . .

# Temp uploads dir (created at runtime by config; explicit for clarity)
RUN mkdir -p temp_uploads

EXPOSE 8000

# Run FastAPI with uvicorn – bind to 0.0.0.0 for container access
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
