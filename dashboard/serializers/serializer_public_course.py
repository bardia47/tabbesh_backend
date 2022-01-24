from rest_framework import serializers
from dashboard.models.course import Course
from accounts.models.user import User
from accounts.models.grade import Grade
from dashboard.models.suggestion import Suggestion
from home.serializers.serializer_course_home import CourseHomeSerializer


class CourseSerializer(CourseHomeSerializer):
    lesson = serializers.ReadOnlyField(source='lesson.title')
    grades = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ('teacher', 'image', 'start_date', 'end_date', 'lesson', 'description',
                  'slug', 'private_description', 'is_active', 'grades', 'acquaintance_video', 'status',
                  'amount')



class CourseSugesstionSerializer(serializers.ModelSerializer):
    course_full_name = serializers.ReadOnlyField(source='course.get_course_full_name')

    class Meta:
        model = Suggestion
        fields = ('first_name', 'course_full_name', 'last_name', 'description', 'course', 'code')

    def create(self, validated_data):
        return Suggestion.objects.create(**validated_data)
