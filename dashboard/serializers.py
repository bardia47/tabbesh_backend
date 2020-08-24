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
    parent = serializers.SerializerMethodField('get_parent_lesson')

    def is_class_active(self, obj):
        next_class = obj.get_next_class()
        if next_class is not None:
            return next_class.is_class_active()
        return False

    def get_first_class(self, obj):
        next_class = obj.get_next_class()
        if next_class is not None:
            return next_class.start_date
        return None

    def get_parent_lesson(self, obj):
        lesson = obj.lesson
        while (True):
            if lesson.parent is None:
                return LessonSerializer(instance=lesson).data
            else:
                lesson = lesson.parent

    class Meta:
        model = Course
        fields = ('code', 'title', 'start_date', 'end_date', 'image', 'teacher', 'url',
                  'is_active', 'first_class', 'private_description', 'parent')


class CourseCalendarSerializer(JSONFormSerializer, serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField('get_is_active')

    class Meta:
        model = Course_Calendar
        fields = ('start_date', 'is_active')

    def get_is_active(self, obj):
        return obj.is_class_active()

    def to_representation(self, course_calendar):
        data = super(CourseCalendarSerializer, self).to_representation(course_calendar)
        course = CourseLessonsSerializer(instance=course_calendar.course)
        data.update(course.data)
        return data


class DashboardSerializer(serializers.Serializer):
    course_calendars = CourseCalendarSerializer(many=True)
    now = serializers.DateTimeField()
    calendar_time = serializers.DurationField(required=False, allow_null=True)


# for shopping page
class ShoppingSerializer(serializers.Serializer):
    teachers = TeacherSerializer(many=True)
    lessons = LessonSerializer(many=True)
    grades = GradeSerializer(many=True)


# for shopping page
class ShoppingCourseSerializer(CourseLessonsSerializer):
    course_calendars = serializers.SerializerMethodField('get_start_dates')
    discount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Course
        fields = ('id', 'title', 'start_date', 'end_date', 'code', 'amount', 'description', 'image', 'teacher',
                  'course_calendars', 'parent','discount')

    def get_start_dates(self, obj):
        dates = []
        calendars = obj.course_calendar_set.all()
        for i in calendars:
            dates.append(i.start_date)
        return dates

    def get_parent_lesson(self, obj):
        return LessonSerializer(instance=obj.get_parent_lesson()).data

    def get_discount(self, obj):
        discount=obj.get_discount()
        if discount:
            return DiscountSerializer(instance=discount).data
        return None


class UserProfileSerializer(JSONFormSerializer, serializers.ModelSerializer):
    grade = serializers.SerializerMethodField('get_student_grade')
    cityTitle = serializers.SerializerMethodField('get_city_title')
    phone_number=serializers.CharField(read_only=True)
    credit = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'username','email', 'grade', 'cityTitle', 'gender', 'national_code', 'phone_number','grades', 'city', 'avatar','credit')

    def get_student_grade(self, obj):
        return obj.get_student_grade()

    def get_city_title(self, obj):
        try:
            return obj.city.title
        except:
            return ""


    def validate_username(self, value):
            user = User.objects.filter(Q(username=value.lower())).exclude(id=self.instance.id)
            if user.exists():
                raise serializers.ValidationError('کاربر با این نام کاربری از قبل موجود است.')
            return value.lower()



# for get method
class UserProfileShowSerializer(serializers.Serializer):

    user = UserProfileSerializer()
    grades = GradeSerializer(many=True)
    cities = CitySerializer(many=True)

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('percent','end_date','title')


class DocumentSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_full_name')
    upload_date_decorated = serializers.SerializerMethodField('get_upload_date_decorated')

    class Meta:
        model = Document
        read_only_fields = ('upload_date',)
        fields = ['sender_name', 'title', 'sender', 'course', 'upload_date', 'upload_date_decorated', 'description', 'upload_document']

    def get_sender_full_name(self, obj):
        return obj.sender.get_full_name()

    def get_upload_date_decorated(self, obj):
        return obj.upload_date_decorated()


class FilesSerializer(serializers.Serializer):
    course = CourseBriefSerializer()
    documents = DocumentSerializer(many=True)


class StudentBriefSerializer(UserProfileSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'grade', 'cityTitle')


class ClassListSerializer(serializers.Serializer):
    course = CourseBriefSerializer()
    students = StudentBriefSerializer(many=True)
