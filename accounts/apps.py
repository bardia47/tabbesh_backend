from django.apps import AppConfig
from . import scheduler


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "حساب های کاربری "

    # run scheduler when app is ready
    def ready(self):
        scheduler.start()