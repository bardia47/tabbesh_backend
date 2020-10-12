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
    teacher = serializers.ReadOnlyField(source='teacher.get_full_name')

    class Meta:
        model = Course
        fields = ('teacher', 'title', 'image')


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
        while True:
            if lesson.parent is None:
                return LessonSerializer(instance=lesson).data
            else:
                lesson = lesson.parent

    class Meta:
        model = Course
        fields = ('id', 'code', 'title', 'start_date', 'end_date', 'image', 'teacher', 'url',
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


# TODO use this after react
class DashoboardInstallmentSerializer(serializers.Serializer):
    ids = serializers.CharField()
    titles = serializers.CharField()


class DashboardSerializer(serializers.Serializer):
    course_calendars = CourseCalendarSerializer(many=True)
    now = serializers.DateTimeField()
    calendar_time = serializers.DurationField(required=False, allow_null=True)
    need_buy = DashoboardInstallmentSerializer(many=False)


# for shopping page
class ShoppingSerializer(serializers.Serializer):
    teachers = TeacherSerializer(many=True)
    lessons = LessonSerializer(many=True)
    grades = GradeSerializer(many=True)


# for shopping page
class ShoppingCourseSerializer(CourseLessonsSerializer):
    course_calendars = serializers.SerializerMethodField('get_start_dates')
    discount = serializers.SerializerMethodField('get_discount')
    installment = serializers.SerializerMethodField('get_installment')

    class Meta:
        model = Course
        fields = ("installment", 'title', 'start_date', 'end_date', 'id', 'description', 'image', 'teacher',
                  'course_calendars', 'parent', 'discount')

    def get_start_dates(self, obj):
        dates = []
        calendars = obj.course_calendar_set.all()
        for i in calendars:
            dates.append(i.start_date)
        return dates

    def get_parent_lesson(self, obj):
        return LessonSerializer(instance=obj.get_parent_lesson()).data

    def get_discount(self, obj):
        discount = obj.get_discount()
        if discount:
            return DiscountSerializer(instance=discount).data
        return None

    def get_installment(self, obj):
        installment = obj.get_next_installment()
        if installment:
            return InstallmentSerializer(instance=installment).data
        return None


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('percent', 'end_date', 'title')


class InstallmentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Installment
        fields = ('id', 'title', 'amount', 'start_date', 'end_date')

    def get_title(self, obj):
        if obj.course.installment_set.all().count() == 1:
            return None
        return obj.title


class UserProfileSerializer(UserBaseSerializer):
    grade = serializers.ReadOnlyField(source='student_grade')
    cityTitle = serializers.ReadOnlyField(source='city.title')
    phone_number = serializers.CharField(read_only=True)
    credit = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'username', 'email', 'grade', 'cityTitle', 'gender', 'national_code', 'phone_number',
                  'grades', 'city', 'avatar', 'credit')


# for get method
class UserProfileShowSerializer(serializers.Serializer):
    user = UserProfileSerializer()
    grades = GradeSerializer(many=True)
    cities = CitySerializer(many=True)


class DocumentSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.get_full_name')
    upload_date_decorated = serializers.ReadOnlyField()

    class Meta:
        model = Document
        read_only_fields = ('upload_date',)
        fields = ['id', 'sender_name', 'title', 'sender', 'course', 'upload_date', 'upload_date_decorated',
                  'description',
                  'upload_document']


class FilesSerializer(serializers.Serializer):
    course = CourseBriefSerializer()
    documents = DocumentSerializer(many=True)


class StudentBriefSerializer(UserProfileSerializer):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'grade', 'cityTitle')


class ClassListSerializer(serializers.Serializer):
    course = CourseBriefSerializer()
    students = StudentBriefSerializer(many=True)


class UserInstallmentSerializer(InstallmentSerializer):
    is_bought = serializers.SerializerMethodField('get_is_bought')
    is_disable = serializers.SerializerMethodField('get_is_disable')

    class Meta:
        model = Installment
        fields = ('id', 'title', 'amount', 'start_date', 'end_date', 'is_bought', 'is_disable')

    def get_is_bought(self, obj):
        if obj.user_set.filter(pk=self.context['request'].user.pk).exists():
            return True
        return False

    def get_is_disable(self, obj):
        now = datetime.datetime.now().date()
        return not ((obj.start_date > now) | (obj.end_date > (now + datetime.timedelta(days=10))))
