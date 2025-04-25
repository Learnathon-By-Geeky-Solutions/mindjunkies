#!/bin/bash
cd /app/

uv run python manage.py collectstatic --noinput
