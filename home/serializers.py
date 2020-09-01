from accounts.models import *
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    grade_choice = serializers.SerializerMethodField('get_choices')

    class Meta:
        model = User
        fields = ('id', 'avatar', 'get_full_name', 'grade_choice')

    def get_choices(self, instance):
        all_grades = instance.grades.all()
        grades = set()
        for grade in all_grades:
            grades.add(grade.get_grade_choice_display())
        return grades


class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    course_title = serializers.ReadOnlyField(source='title')
    grade_id = serializers.ReadOnlyField(source='grade.id')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title', 'grade_id')


class CourseDiscountedSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    course_title = serializers.ReadOnlyField(source='title')
    grade_id = serializers.ReadOnlyField(source='grade.id')
    percent = serializers.SerializerMethodField('get_discount_percent')
    discount_name = serializers.SerializerMethodField('get_discount_name')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title', 'grade_id', 'percent', 'discount_name')

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
