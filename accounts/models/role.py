from accounts.apps import AccountsConfig
from core.models import AbstractBaseModel

class Role(AbstractBaseModel):
    class Meta:
        verbose_name_plural = "نقش"
        verbose_name = "نقش"
        app_label = AccountsConfig.name
