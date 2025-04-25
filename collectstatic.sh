#!/bin/bash
cd /app/

uv run python manage.py tailwind build
uv run python manage.py collectstatic --noinput
