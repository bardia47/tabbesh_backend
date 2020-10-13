from accounts.models import *
from .enums import AdminEnums
from core.utils import TextUtils
from django.contrib import messages
from accounts.enums import InstallmentModelEnum

class AdminValidator():
    def showErrorsOfCourse(obj, request):
        if (obj):
            if (obj.course_calendar_set.count() == 0):
                messages.warning(request,
                                     TextUtils.replacer(AdminEnums.courseCalendarWarning.value, [obj.title]))
            now = datetime.datetime.now()
            if (obj.end_date > now + datetime.timedelta(days=InstallmentModelEnum.installmentDateBefore.value)):
                if (not obj.get_next_installment()):
                    messages.error(request,
                                         TextUtils.replacer(AdminEnums.noInstallmentError.value, [obj.title]))
                elif (obj.installment_set.latest('end_date').end_date < obj.end_date.date()):
                    messages.error(request,
                                         TextUtils.replacer(AdminEnums.installmentEndDateError.value, [obj.title]))