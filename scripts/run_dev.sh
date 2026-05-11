#!/bin/sh

cd /app/backend

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate

uvicorn messenger.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --reload