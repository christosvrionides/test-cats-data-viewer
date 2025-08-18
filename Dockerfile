# ---- Stage 1: Build Frontend Assets ----
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend

# Copy frontend package files and install dependencies
COPY package*.json ./
RUN npm install

# ---- Stage 2: Final Python Application Image ----
FROM python:3.11-slim

# Avoid writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install OS dependencies for psycopg (PostgreSQL driver) and curl
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Collect static files inside the container
RUN python manage.py collectstatic --noinput

# Copy frontend assets from frontend-builder stage
COPY --from=frontend-builder /frontend/node_modules/govuk-frontend/dist/govuk/assets /app/static/assets
COPY --from=frontend-builder /frontend/node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.css /app/static/govuk-frontend/dist/govuk/
COPY --from=frontend-builder /frontend/node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.js /app/static/govuk-frontend/dist/govuk/

# Expose port 8000
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "uploader_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--reload"]
