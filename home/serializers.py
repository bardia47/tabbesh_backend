from accounts.models import *
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    grade_choice = serializers.SerializerMethodField('get_first_choice')

    class Meta:
        model = User
        fields = ('avatar', 'get_full_name', 'grade_choice')

    def get_first_choice(self, instance):
        # grades = instance.grades.values('grade_choice')
        grades = instance.grades.all()
        if len(grades) > 0:
            choice_field = grades.first().get_grade_choice_display()
            return choice_field
        # return grades


class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    course_title = serializers.ReadOnlyField(source='title')
    grade_id = serializers.ReadOnlyField(source='grade.id')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'course_title', 'grade_id')


class CourseSerializerTitle(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title',)
