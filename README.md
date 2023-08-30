# python-kublo
# Building

Building by command - docker-compose build

It will create django restful project and database

# Opening

Just open it by command - docker-compose up

It'll make some actions
1. It'll run custom command that waits for database to avoid situation when database is not ready and django sends some requests there. Project can crush
2. Then it'll check code on PEP8 by flake
3. Then it'll run unit tests
4. Then it'll migrate database
5. And finally it'll run server

# Some useful information

If you want to run any other commands use syntax:
docker-compose run --rm app sh -c "flake8" - it'll run flake8 check
docker-compose run --rm app sh -c "python manage.py test" - it'll run unit tests
docker-compose run --rm app sh -c "python manage.py makemigrations" - it'll make migration file
docker-compose run --rm app sh -c "python manage.py createsuperuser" - it'll create superuser

# Navigation
127.0.0.1:8000/admin - admin page
127.0.0.1:8000/create - user creating page

