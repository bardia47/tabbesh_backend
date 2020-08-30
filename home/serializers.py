from accounts.models import *
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    grade_choice = serializers.SerializerMethodField('get_choices')

    class Meta:
        model = User
        fields = ('avatar', 'get_full_name', 'grade_choice')

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


class CourseSerializerTitle(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title',)
