#!/usr/bin/bash
APP_PORT=${APP_PORT:-8080}
cd /app/
uv run gunicorn --worker-tmp-dir /dev/shm project.wsgi:application --bind "0.0.0.0:${APP_PORT}"
