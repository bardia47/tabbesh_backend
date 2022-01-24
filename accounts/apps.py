from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "accounts"

    # def ready(self):
    #     import core.signals