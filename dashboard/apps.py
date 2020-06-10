from django.apps import AppConfig
from . import scheduler


class DashboardConfig(AppConfig):
    name = 'dashboard'

    # run scheduler when app is ready
    def ready(self):
        scheduler.start()
