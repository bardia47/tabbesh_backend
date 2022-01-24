# Grade Models
from django.db import models
from accounts.apps import AccountsConfig
from core.models import AbstractBaseModel


class Grade(AbstractBaseModel):
    First = 'FIRST'
    Second = 'SECOND'
    Third = 'THIRD'
    Other = 'OTHER'
    Grade_CHOICES = ((First, 'ابتدایی'), (Second, 'متوسطه اول'), (Third, 'متوسطه دوم'),
                     (Other, 'مهارتی'))
    grade_choice = models.CharField(
        "پایه", max_length=10, choices=Grade_CHOICES, default='Other')

    class Meta:
        ordering = ['code']
        verbose_name_plural = "پایه"
        verbose_name = "پایه"
        app_label = AccountsConfig.name

    def __str__(self):
        return self.title