#!/bin/sh
set -e
until cd /python-kublo
do
  echo "Wait for server volume..."
done

# Adjust the path to manage.py based on its new location
until python manage.py migrate
do
  echo "Waiting for postgres ready"
done

# Run tests
echo "Running tests..."
# If tests fail, exit the script
if python manage.py test; then
  echo "Tests passed."
else
  echo "Tests failed, exit."
  exit 1
fi

python manage.py collectstatic --noinput

gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
