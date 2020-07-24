from django.contrib.auth.models import User
from accounts.models import *
from accounts.serializers import *

from rest_framework import serializers
from html_json_forms.serializers import JSONFormSerializer
from pip._vendor.pkg_resources import require
from django.contrib.auth.hashers import make_password


class TeacherSerializer(JSONFormSerializer, serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_user_full_name')

    class Meta:
        model = Course
        fields = ('id', 'full_name')

    def get_user_full_name(self, obj):
        return obj.get_full_name()


class LessonSerializer(JSONFormSerializer, serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title')


class GradeSerializer(JSONFormSerializer, serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'title')


class CourseBriefSerializer(JSONFormSerializer, serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField('get_user_full_name')

    class Meta:
        model = Course
        fields = ('teacher', 'title', 'image')

    def get_user_full_name(self, obj):
        return obj.teacher.get_full_name()


class CourseLessonsSerializer(CourseBriefSerializer):
    first_class = serializers.SerializerMethodField('get_first_class')
    is_active = serializers.SerializerMethodField('is_class_active')

    def is_class_active(self, obj):
        return obj.get_next_class().is_class_active()

    def get_first_class(self, obj):
        return obj.get_next_class().start_date

    class Meta:
        model = Course
        fields = ('code','title', 'start_date', 'end_date' ,'image', 'teacher','url' ,
                  'is_active','first_class', 'description')


class CourseCalendarSerializer(JSONFormSerializer, serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField('get_is_active')

    class Meta:
        model = Course_Calendar
        fields = ('start_date','is_active')

    def get_is_active(self, obj):
        return obj.is_class_active()

    def to_representation(self, course_calendar):
        data =  super(CourseCalendarSerializer, self).to_representation(course_calendar)
        course=CourseLessonsSerializer(instance=course_calendar.course)
        data.update(course.data)
        return data


class DashboardSerializer(serializers.Serializer):
    course_calendars = CourseCalendarSerializer(many=True)
    now = serializers.DateTimeField()
    calendar_time = serializers.DurationField(required=False, allow_null=True)


#for shopping page
class ShoppingSerializer(serializers.Serializer):
    teachers = TeacherSerializer(many=True)
    lessons = LessonSerializer(many=True)
    grades = GradeSerializer(many=True)


#for shopping page
class ShoppingCourseSerializer(CourseLessonsSerializer):
    course_calendars = serializers.SerializerMethodField('get_start_dates')

    class Meta:
        model = Course
        fields = ('id', 'title', 'start_date', 'end_date', 'code', 'amount', 'description', 'image', 'teacher',
                  'course_calendars')
        fields = ('title', 'start_date', 'end_date', 'code', 'amount', 'description', 'image', 'teacher', 'course_calendars')

    def get_start_dates(self, obj):
        dates = []
        calendars = obj.course_calendar_set.all()
        for i in calendars:
            dates.append(i.start_date)
        return dates


class UserProfileSerializer(JSONFormSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'username', 'email', 'grades', 'gender', 'phone_number', 'city', 'avatar')
    grade = serializers.SerializerMethodField('get_student_grade')
    cityTitle = serializers.SerializerMethodField('get_city_title')

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'username', 'grade', 'cityTitle', 'gender', 'national_code', 'phone_number', 'avatar')

    def get_student_grade(self, obj):
            try:
                return obj.grades.all().first().title
            except:
                return ""

    def get_city_title(self, obj):
            try:
                return obj.city.title
            except:
                return ""

                # for post method and android
class UserSaveProfileSerializer(UserProfileSerializer):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'username', 'email', 'gender', 'national_code',
                  'grades', 'city', 'avatar')

    # for get method


class UserProfileShowSerializer(serializers.Serializer):
    user = UserProfileSerializer()
    grades = GradeSerializer(many=True)
    cities = CitySerializer(many=True)
