"""
command that waits for db available to avoid crush app in case
if db will be not connected first
call it 'python manage.py wait_for_db'
"""

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """represents wait_for_db command"""

    def handle(self, *args, **options):
        """entrypoint for command"""
        self.stdout.write('Waiting for db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('waiting 1 sec more')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
