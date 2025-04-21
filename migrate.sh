#!/usr/bin/bash

DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"shafayet.sadi@gmail.com"}
cd /app/

uv run python manage.py migrate --noinput || true
uv run python manage.py createsuperuser --email "$DJANGO_SUPERUSER_EMAIL" --noinput || true