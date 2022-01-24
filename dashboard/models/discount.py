from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import AbstractBaseModel


class Discount(AbstractBaseModel):
    percent = models.IntegerField('درصد',
                                  default=10,
                                  validators=[
                                      MaxValueValidator(100),
                                      MinValueValidator(1)
                                  ]
                                  )
    start_date = models.DateTimeField('تاریخ شروع')
    end_date = models.DateTimeField('تاریخ پایان', null=True, blank=True)
    courses = models.ManyToManyField(
        'Course', blank=True, verbose_name='درس های تخفیف خورده')

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "تخفیف"
        verbose_name = "تخفیف"

    def __str__(self):
        return str(self.title)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError(
                'تاریخ پایان باید پس از تاریخ شروع باشد یا خالی باشد')


class DiscountWithoutCode(Discount):
    class Meta:
        proxy = True
        verbose_name = 'تخفیف بدون کد'
        verbose_name_plural = 'تخفیف بدون کد'
