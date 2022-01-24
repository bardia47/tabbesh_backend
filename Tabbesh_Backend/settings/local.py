import sys
from .base import *

DEBUG = True


if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    CACHES['default']['LOCATION'] = "redis://{0}:6379/2".format(env("REDIS_HOST")),




