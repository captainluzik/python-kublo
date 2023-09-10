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

export DJANGO_TEST_DB_REMOVAL=yes
if python manage.py test --failfast --no-input; then
    echo "Django tests passed"
else
    echo "Django tests failed"
    exit
fi

python manage.py loaddata sectors.json

gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
