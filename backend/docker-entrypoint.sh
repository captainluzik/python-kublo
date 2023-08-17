#!/bin/sh
set -e
until cd /djangoChallenge
do
  echo "Wait for server volume..."
done

# Adjust the path to manage.py based on its new location
until python manage.py migrate
do
  echo "Waiting for postgres ready"
done

python manage.py collectstatic --noinput

gunicorn djangoChallenge.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
