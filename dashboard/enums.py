from enum import Enum


class DashboardMessages(Enum):
    needBuyMassage = 'شهریه آتی درس (دروس) {0} پرداخت نشده است'


class AdminEnums(Enum):
    courseCalendarWarning = 'دوره {0} زمان برگذاری ندارد'
    noInstallmentError = 'دوره {0} قسط آتی ندارد و در صفحه خرید درس نمایش داده نمیشود'
    installmentEndDateError = ' قسط های دوره {0} تا پایان زمان برگذاری دوره نمیباشد'
