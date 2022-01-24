from django.db import models
# Lesson Model
from core.models import AbstractBaseModel

class Lesson(AbstractBaseModel):
    grades = models.ManyToManyField('accounts.Grade', blank=True, verbose_name="پایه")
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="درس پدر")
    unique_together = [['title', 'grade']]

    class Meta:
        verbose_name_plural = "درس"
        verbose_name = "درس"