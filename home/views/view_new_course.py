from datetime import datetime
from rest_framework import generics

from dashboard.models import Course
from home.serializers.serializer_course_home import CourseHomeSerializer


class NewCourseHome(generics.ListAPIView):
    serializer_class = CourseHomeSerializer
    pagination_class = None

    def get_queryset(self):
        time_now = datetime.now()
        # this is forbidden code
        return Course.objects.filter(is_active=True, end_date__gte=time_now).order_by('-id')[:12]
