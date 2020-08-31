from enum import Enum
from accounts.models import Event


class ZarinPal(Enum):
    descriptionText = 'دوره(های) {0} {1} توسط {2} خریداری شد'
    dicountText = 'با کد تخفیف {0}'
    eventText = 'به مناسبت {0} با {1} درصد تخفیف'


class Events(Enum):
    # this is percent
    INING_DISCOUNT = 10
    # this is amount
    INING_AMOUNT = 10000
