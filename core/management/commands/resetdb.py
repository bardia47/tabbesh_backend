import os
import glob
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Resets the database'

    def handle(self, *args, **options):
        dbname = settings.DATABASES["default"]["NAME"]

        cursor = connection.cursor()
        cursor.execute('show tables;')
        parts = ('DROP TABLE IF EXISTS %s;' % table for (table,) in cursor.fetchall())
        sql = 'SET FOREIGN_KEY_CHECKS = 0;\n' + '\n'.join(parts) + 'SET FOREIGN_KEY_CHECKS = 1;\n'
        connection.cursor().execute(sql)
        apps = [app for app in settings.INSTALLED_APPS
                if app.endswith('Config')]
        sep = os.sep
        for app in apps:
            name = app.split('.')[0]
            try:
                dir = settings.BASE_DIR + sep + name + sep + "migrations" + sep
                shutil.rmtree(dir)
            except:
                print(dir + " not found")
            os.system("python manage.py makemigrations %s" % name)
        os.system("python manage.py migrate")
        # load fixtures
        #  os.system("python manage.py newmigrate")
        fixtures = glob.glob(settings.BASE_DIR + sep + "*" + sep + "fixtures" + sep + "*.json")
        for fixture in fixtures:
            os.system("python manage.py loaddata " + fixture)
