# class Pay_History(models.Model):
#     purchaser = models.ForeignKey(
#         'User', on_delete=models.DO_NOTHING, verbose_name="خریدار")
#     amount = models.FloatField("هزینه", default=float(0))
#     is_successful = models.BooleanField('موفق', default=False)
#     submit_date = models.DateTimeField("تاریخ ثبت", null=True)
#     installments = models.TextField()
#     payment_code = models.CharField("شناسه پرداخت", max_length=20)
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name_plural = "سوابق خرید"
#         verbose_name = "سوابق خرید"
#
#     def submit_date_decorated(self):
#         if self.submit_date:
#             return datetime2jalali(self.submit_date).strftime('%y/%m/%d _ %H:%M:%S')
#         else:
#             "-"
#
#     def get_installments(self):
#         installments_id_list = self.installments.split()
#         return list(Installment.objects.filter(id__in=installments_id_list).annotate(
#             full_title=Concat('title', V(' '), 'course__title')).values_list('full_title', flat=True))
#
#     get_installments.short_description = 'قسط های خریداری شده'
#     submit_date_decorated.short_description = 'تاریخ ثبت'
