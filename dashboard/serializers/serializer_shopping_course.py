# for shopping page
from rest_framework import serializers

from dashboard.models import Course ,Course_Calendar
from dashboard.models.discount import Discount


class CourseCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Calendar
        fields = ('end_date', 'start_date')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('percent', 'end_date', 'title')

class ShoppingCourseSerializer(serializers.ModelSerializer):
    course_calendars = CourseCalendarSerializer(source='get_first_week_dates',many=True)
    discount = DiscountSerializer(read_only=True)
    amount = serializers.ReadOnlyField(source='amount_payable')

    class Meta:
        model = Course
        fields = ('title', 'start_date', 'end_date', 'id', 'description', 'image', 'teacher',
                  'course_calendars', 'discount', 'amount')

