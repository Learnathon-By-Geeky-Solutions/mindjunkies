#!/bin/bash
cd /app/

uv run python manage.py migrate --noinput || true
uv run python manage.py create_superuser