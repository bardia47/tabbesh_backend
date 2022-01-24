import os
import glob
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps


class Command(BaseCommand):
    help = 'migrate for circular problem'

    def handle(self, *args, **options):
        base = str(settings.BASE_DIR)
        apps = [app for app in settings.INSTALLED_APPS
         if app.endswith('Config')]
        bad_words = ['ManyToManyField', 'ForeignKey']
        for num in range(0,len(apps)-1):
            name = apps[num].split('.')[0]
            os.system("python manage.py makemigrations %s" % name)
            list_of_files = glob.glob(name+'/migrations'+'/*')  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)
            print(latest_file+'.')
            with open(latest_file, encoding="utf8") as oldfile, open(latest_file+'.', 'w', encoding="utf8") as newfile:
                for line in oldfile:
                    if not any(bad_word in line for bad_word in bad_words):
                        newfile.write(line)
            os.remove(latest_file)
            os.rename(latest_file+'.', latest_file)
        os.system("python manage.py migrate")
