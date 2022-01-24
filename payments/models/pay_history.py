from django.db import models
from django.db.models.functions import Concat
from django.db.models import Value as V
from jalali_date import datetime2jalali

from dashboard.models import Installment
from payments.apps import PaymentsConfig


class Pay_History(models.Model):
    purchaser = models.ForeignKey(
        'accounts.User', on_delete=models.DO_NOTHING, verbose_name="خریدار")
    amount = models.FloatField("هزینه", default=float(0))
    is_successful = models.BooleanField('موفق', default=False)
    submit_date = models.DateTimeField("تاریخ ثبت", null=True)
    # installments = models.CommaSeparatedIntegerField(max_length=10000)
    payment_code = models.CharField("شناسه پرداخت", max_length=20)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "سوابق خرید"
        verbose_name = "سوابق خرید"
        app_label = PaymentsConfig.name

    def submit_date_decorated(self):
        if self.submit_date:
            return datetime2jalali(self.submit_date).strftime('%y/%m/%d _ %H:%M:%S')
        else:
            "-"

    def get_installments(self):
        installments_id_list = self.installments.split(',')
        return list(Installment.objects.filter(id__in=installments_id_list).annotate(
            full_title=Concat('title', V(' '), 'course__title')).values_list('full_title', flat=True))

    get_installments.short_description = 'قسط های خریداری شده'
    submit_date_decorated.short_description = 'تاریخ ثبت'
