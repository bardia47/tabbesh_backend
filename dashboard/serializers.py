from django.contrib.auth.models import User
from accounts.models import *
from rest_framework import serializers
from html_json_forms.serializers import JSONFormSerializer
from pip._vendor.pkg_resources import require
from django.contrib.auth.hashers import make_password

class CourseCalendarSerializer(JSONFormSerializer,serializers.ModelSerializer):
   
    class Meta:
        model = Course_Calendar
        fields = ('__all__')
        depth=3

class DashboardSerializer(serializers.Serializer):
    course_calendars=CourseCalendarSerializer(many=True,read_only=True)
    now = serializers.DateTimeField()
    calendar_time=serializers.DurationField(required=False,allow_null=True)
    
