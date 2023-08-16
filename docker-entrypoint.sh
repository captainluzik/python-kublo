#!/bin/sh
set -e
until cd /app
do
    echo "Wait for server volume..."
done

until python manage.py migrate
do
    echo "Waiting for postgres ready..."
done

python manage.py collectstatic --noinput

python manage.py runserver
