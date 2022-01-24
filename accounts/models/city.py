from accounts.apps import AccountsConfig
from core.models import AbstractBaseModel

class City(AbstractBaseModel):
    class Meta:
        verbose_name_plural = "شهر"
        verbose_name = "شهر"
        app_label = AccountsConfig.name