# Installment model Model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from dashboard.apps import DashboardConfig


class Installment(models.Model):
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE, verbose_name="دوره")
    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان")
    title = models.CharField("عنوان", max_length=30)
    amount = models.FloatField("مبلغ", default=float(0),
                               validators=[MinValueValidator(0)]
                               )
    users = models.ManyToManyField('accounts.User', blank=True)


    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "قسط"
        verbose_name = "قسط"
        app_label = DashboardConfig.name

    def __str__(self):
        return self.title + " " + self.course.title

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.start_date or not self.end_date or self.end_date < self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")
        if self.start_date < self.course.start_date or self.end_date > self.course.end_date:
            raise ValidationError("تاریخ قسط قبل / بعد از تاریخ دوره است")
        query = Q(course__id=self.course.id)
        if self.id is not None:
            query &= ~Q(id=self.id)
        query &= ((Q(start_date__gte=self.start_date) & (Q(end_date__lte=self.end_date))) |
                  (Q(start_date__lte=self.start_date) & (Q(end_date__gte=self.end_date))) |
                  ((Q(start_date__lte=self.start_date)) & (Q(end_date__gte=self.start_date))) |
                  (Q(end_date__gte=self.end_date) & (Q(end_date__lte=self.end_date)))
                  )
        if Installment.objects.filter(query).exists():
            raise ValidationError("تاریخ قسط تداخل دارد")

    @property
    def amount_payable(self):
        discount = self.course.discount()
        if discount:
            return self.amount * (100 - discount.percent) / 100
        return self.amount
