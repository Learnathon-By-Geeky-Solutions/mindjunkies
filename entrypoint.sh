#!/bin/bash
APP_PORT=${APP_PORT:-8080}
cd /app/

uv run python manage.py tailwind build
uv run python manage.py collectstatic --noinput
uv run gunicorn --worker-tmp-dir /dev/shm project.wsgi:application --bind "0.0.0.0:${APP_PORT}"
