from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from dashboard.serializers.serializer_public_course import CourseSerializer, CourseSugesstionSerializer
from dashboard.models.course import Course
from dashboard.models.suggestion import Suggestion
from rest_framework.response import Response
from rest_framework import status


class PublicCourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'slug'
    http_method_names = ['get']


class PublicCourseSugesstionsView(viewsets.ModelViewSet):
    serializer_class = CourseSugesstionSerializer
    queryset = Suggestion.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get','post']

    def create(self, request, *args, **kwargs):
        course = Course.objects.get(slug=kwargs['pk_slug']).id
        request.data['course_id'] = course
        serializer = CourseSugesstionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)




