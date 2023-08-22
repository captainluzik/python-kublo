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

export DJANGO_TEST_DB_REMOVAL=yes

if python manage.py test --failfast; then
  echo "All tests passed"
else
  echo "Tests failed"
  exit
fi

#python manage.py test

python manage.py collectstatic --no-input

gunicorn core.wsgi:application --bind 0.0.0.0 --workers 4 --threads 4
