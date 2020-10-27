from django.core.management.base import BaseCommand
from django.core import management

class Command(BaseCommand):
    help = 'run server on local ' \
           'makemigrations' \
           'migrate' \
           'pip install' \
           'runserver'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            'ip', nargs='?',
            help='ip and port',
        )

    def handle(self, *args, **kwargs):
        try:
            management.call_command('dbbackup')
            management.call_command('makemigrations')
            management.call_command('migrate')
            management.call_command('shell',command='import subprocess;import sys;subprocess.run("pip install -r requirements.txt");')
            #management.call_command('collectstatic')
            # management.call_command('check','--deploy')
            # management.call_command('test')
            port = 'localhost:8000'
            if kwargs['ip']:
                port = kwargs['ip']
            management.call_command('runserver',port)

        except Exception as e:
            self.stdout.write(self.style.ERROR(print(e)))
