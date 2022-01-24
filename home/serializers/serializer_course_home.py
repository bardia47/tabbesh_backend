from rest_framework import serializers

from dashboard.models import Course


class CourseHomeSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.get_full_name')
    class Meta:
        model = Course
        fields = ('id', 'image', 'teacher', 'title')