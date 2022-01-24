from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.models.user import User
from dashboard.models import Course_Header, Course, Course_Calendar
from dashboard.serializers.serializer_course import PanelCoursesSerializer, OfflineVideoSerializer, \
    CourseCalenderSerializer
from datetime import datetime


class PanelCoursesView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PanelCoursesSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).courses()


class CourseCalenderView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseCalenderSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        try:
            course = Course.objects.get(slug=self.kwargs['pk_slug'])
            return Course_Calendar.objects.filter(course_id=course.id)
        except:
            return None


class OfflineVideoView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OfflineVideoSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        try:
            course = Course.objects.get(slug=self.kwargs['pk_slug'], end_date__gt=datetime.now())
            return Course_Header.objects.filter(course_id=course.id)
        except:
            return None
