# Stage 1: Build
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first, install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set env for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port (per Kubernetes)
EXPOSE 5000

# CMD: Run Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]