from rest_framework import serializers
from accounts.models.user import User, TeacherUser
from accounts.models.grade import Grade
from dashboard.models.course import Course
from django.db.models import Q
from datetime import datetime

class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')
    grades = serializers.SerializerMethodField()
    # suggestions = serializers.SerializerMethodField()

    class Meta:
        model = TeacherUser
        fields = ('full_name','avatar','description','grades',)

    # def get_courses(self,instance):
    #     teacher_courses_list = []
    #     teacher_courses = instance.course_set.all()
    #     for teacher_course in teacher_courses:
    #         teacher_course_dict = {'course_name':str(teacher_course.get_course_full_name),
    #                                'description':teacher_course.description}
    #         teacher_courses_list.append(teacher_course_dict)
    #     return teacher_courses_list

    def get_grades(self, instance):
        teacher_grades_list = []
        teacher_grades = instance.grades.all()
        for teacher_grade in teacher_grades:
            teacher_grades_list.append(teacher_grade.title)
        return teacher_grades_list

