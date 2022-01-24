# the courses that user is purchased
from rest_framework import serializers
from accounts.models.user import User
from dashboard.models.course import Course
from dashboard.enums.enum_statusclass import StatusClass
from dashboard.models.course_calendar import Course_Calendar
import datetime


class UserCourseCalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Calendar
        fields = ('start_date', 'end_date')


class UserCoursesSerializer(serializers.ModelSerializer):
    next_session = UserCourseCalenderSerializer(source='get_first_class')

    class Meta:
        model = Course
        fields = ('title', 'slug', 'next_session', 'url', 'image', 'status')

    # def get_next_session(self, instance):
    #     course_calenders = Course_Calendar.objects.filter(course_id=instance.id)
    #     soonest_classes = course_calenders[0]
    #     for course_calender in course_calenders[1:]:
    #         if soonest_classes.start_date > course_calender.start_date and \
    #                 course_calender.start_date < datetime.datetime.now():
    #             soonest_classes = course_calender
    #     return str(soonest_classes.start_date)
