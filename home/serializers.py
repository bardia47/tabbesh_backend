from accounts.models import *
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar', 'get_full_name', 'grade_choice')


class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.ReadOnlyField(source='teacher.get_full_name')
    lesson_title = serializers.ReadOnlyField(source='lesson.title')
    grade_title = serializers.ReadOnlyField(source='grade.title')

    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher_full_name', 'lesson_title', 'grade_title')