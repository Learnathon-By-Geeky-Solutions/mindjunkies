#!/bin/bash

echo "Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
uv run gunicorn project.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --threads 2 \
    --timeout 120
