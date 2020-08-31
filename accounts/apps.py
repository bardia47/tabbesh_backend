from django.apps import AppConfig
from . import scheduler
import logging


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "حساب های کاربری "

    # run scheduler when app is ready
    def ready(self):
        logger = logging.getLogger("django")
        scheduler.start()
        logger.error("this is not error: scheduler is running")
