# Course_Calendar Model
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from jalali_date import datetime2jalali


class Course_Calendar(models.Model):
    course_header = models.ForeignKey(
        'dashboard.course_header', on_delete=models.CASCADE, verbose_name="سر فصل")
    course = models.ForeignKey(
        'dashboard.course', on_delete=models.CASCADE, verbose_name='دوره'
    )
    start_date = models.DateTimeField("تاریخ شروع")
    end_date = models.DateTimeField("تاریخ پایان")
    video = models.URLField('ویدیو ضبط شده', null=True, blank=True)

    class Meta:
        ordering = ['end_date']
        verbose_name_plural = "زمان برگزاری"
        verbose_name = "زمان برگزاری"

    def __str__(self):
        return self.course.title

    def get_start_date_decorated(self):
        return datetime2jalali(self.start_date).strftime('%y/%m/%d _ %H:%M:%S')

    def get_end_date_decorated(self):
        return datetime2jalali(self.end_date).strftime('%y/%m/%d _ %H:%M:%S')

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'

    def is_class_active(self):
        now = datetime.datetime.now()
        a = now - self.start_date + datetime.timedelta(minutes=5)
        b = now - self.end_date
        if a.total_seconds() >= 0 > b.total_seconds():
            return True
        else:
            return False

    # get soonest class
    def soonest_active_classes(self):
        course_calenders = Course_Calendar.objects.filter(course_id=self.course_id)
        soonest_classes = course_calenders[0]
        for course_calender in course_calenders[1:]:
            if soonest_classes.start_date > course_calender.start_date and \
                    course_calender.start_date < datetime.datetime.now():
                soonest_classes = course_calender
        return soonest_classes

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.start_date or not self.end_date or self.end_date < self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")
