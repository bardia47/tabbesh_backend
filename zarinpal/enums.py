from enum import Enum
from accounts.models import Event


class PaymentMassages(Enum):
    discountMassage = 'تخفیف با موفقیت اعمال شد'
    discountErrorMassage = 'کد تخفیف معتبر نمی باشد دوباره امتحان کنید'


class MERCHANT(Enum):
    merchant = '0c5db223-a20f-4789-8c88-56d78e29ff63'


# for pay desc
class ZarinPal(Enum):
    descriptionText = 'دوره(های) {0} {1} توسط {2} خریداری شد'
    dicountText = 'با کد تخفیف {0}'
    eventText = 'به مناسبت {0} {1} با {2} درصد تخفیف'
    relatedPersonText = '(کاربر مرتبط : {0})'


class Events(Enum):
    # this is percent
    INING_DISCOUNT = 10
    # this is amount
    INING_AMOUNT = 30000
