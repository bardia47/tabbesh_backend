from dashboard.serializers import *
from accounts.models import *
from rest_framework import serializers
from core.fields import SearchHyperlinkField


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    grade_choice = serializers.SerializerMethodField('get_choices')

    class Meta:
        model = TeacherUser
        fields = ('id', 'avatar', 'get_full_name', 'grade_choice', 'url')
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
        }

    def get_choices(self, instance):
        all_grades = instance.grades.all()
        grades = set()
        for grade in all_grades:
            grades.add(grade.get_grade_choice_display())
        return grades


class TeacherDetailSerializer(serializers.HyperlinkedModelSerializer):
    grade_choice = serializers.SerializerMethodField('get_choices')
    courses = serializers.SerializerMethodField('get_courses')
    url = SearchHyperlinkField(view_name='shopping', read_only=True, search_field='id', param_name='teacher')

    class Meta:
        model = TeacherUser
        fields = ('avatar', 'get_full_name', 'grade_choice', 'description', 'courses', 'url')

    def get_courses(self, instance):
        return ShoppingCourseSerializer((instance).get_shopping_courses(), read_only=True, many=True).data

    def get_choices(self, instance):
        grades = set()
        for grade in instance.grades.all():
            grades.add(grade.get_grade_choice_display())
        return grades


class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    course_title = serializers.ReadOnlyField(source='title')
    teacher_id = serializers.ReadOnlyField(source='teacher.id')
    lesson_id = serializers.ReadOnlyField(source='lesson.id')
  #  grade_id = serializers.ReadOnlyField(source='grade.id')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title','teacher_id','lesson_id')


class CourseDiscountedSerializer(CourseSerializer):
   # grade_id = serializers.ReadOnlyField(source='grade.id')
    percent = serializers.SerializerMethodField('get_discount_percent')
    discount_name = serializers.SerializerMethodField('get_discount_name')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title', 'percent', 'discount_name','teacher_id','lesson_id')

    def get_discount_name(self, obj):
        return obj.get_discount().title

    def get_discount_percent(self, obj):
        return obj.get_discount().percent


class CourseSerializerTitle(serializers.Serializer):
    title = serializers.CharField(max_length=50)


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('description',)


class MessageSerializer(serializers.ModelSerializer):
    grade = serializers.ReadOnlyField(source='grade.title')

    class Meta:
        model = Message
        fields = ('name', 'grade', 'message',)


class WeblogDetailSerializer(serializers.ModelSerializer):
    sender = StudentBriefSerializer(read_only=True)
    update_date = serializers.ReadOnlyField(source='update_date_decorated')

    class Meta:
        model = Weblog
        fields = '__all__'


class WeblogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weblog
        fields = ['title', 'image', 'pub_date', 'slug', 'url', 'first_paragraph', ]
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ['image', 'url']
