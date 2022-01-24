from enum import Enum

class InstallmentModelEnum(Enum):
    installmentDateBefore = 10
    installmentIsBought = 'پرداخت شده'
    installmentIsExpired = 'از دست داده اید'
    installmentIsNotBought = 'پرداخت نشده'
    installmentAll = "تمام شهریه"