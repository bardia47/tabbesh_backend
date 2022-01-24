from django.db import models
from core.models import AbstractBaseModel

class Course_Header(AbstractBaseModel):
    course = models.ForeignKey('dashboard.course',on_delete=models.DO_NOTHING,verbose_name='دوره')

    class Meta:
        verbose_name = 'سرفصل'
        verbose_name_plural = 'سر فصل ها'

