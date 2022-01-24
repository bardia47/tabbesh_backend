from django.db import models
from core.models import AbstactDescriptionBaseModel
from dashboard.apps import DashboardConfig
# from dashboard.models.course import Course

class Suggestion(AbstactDescriptionBaseModel):
    # user = models.ForeignKey('accounts.User',on_delete=models.CASCADE,verbose_name='کاربر')
    first_name = models.CharField('نام',max_length=20,null=True,blank=True)
    last_name = models.CharField('نام خانوادگی',max_length=20,null=True,blank=True)
    course = models.ForeignKey('dashboard.Course',on_delete=models.DO_NOTHING,verbose_name='دوره')

    class Meta:
        verbose_name = 'نظرات'
        verbose_name_plural = 'نظرات'
        app_label = DashboardConfig.name

    def get_course(self):
        return self.course.get_course_full_name()

