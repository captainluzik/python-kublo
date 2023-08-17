"""
A command that waits db being available
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Represents command to wait db"""

    def handle(self, *args, **options):
        """Entrypoint"""
        self.stdout.write("Waiting for db...")
        db_up = False
        while db_up==False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Wait a bit more")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("DB is available"))
