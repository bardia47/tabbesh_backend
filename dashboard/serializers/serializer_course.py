from rest_framework import serializers
from dashboard.models import Course, Course_Calendar, Course_Header


class PanelCoursesSerializer(serializers.ModelSerializer):
    teacher_name = serializers.ReadOnlyField(source='teacher.get_full_name')

    # course_calender = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('title', 'slug', 'teacher_name', 'image',)


class CourseCalenderSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='course.url')
    course_header = serializers.ReadOnlyField(source='course_header.title')
    active_class = serializers.ReadOnlyField(source='is_class_active')

    class Meta:
        model = Course_Calendar
        fields = ('url', 'start_date', 'end_date', 'course_header', 'active_class'
                  , 'video')


class OfflineVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = Course_Header
        fields = ('title', 'video')

    def get_video(self, instance):
        course_calender = Course_Calendar.objects.get(course_header=instance)
        return course_calender.video