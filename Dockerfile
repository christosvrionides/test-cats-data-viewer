# ---- Stage 1: Build Frontend Assets ----
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY package*.json ./
RUN npm install

# ---- Stage 2: Final Python Application Image ----
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code
COPY . .

# Collect static files inside the container
RUN python manage.py collectstatic --noinput

# Create the static directory and copy the assets into it
# This is the step that was not happening before
COPY --from=frontend-builder /frontend/node_modules/govuk-frontend/dist/govuk/assets /app/static/assets
COPY --from=frontend-builder /frontend/node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.css /app/static/govuk-frontend/dist/govuk/
COPY --from=frontend-builder /frontend/node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.js /app/static/govuk-frontend/dist/govuk/