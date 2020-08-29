from django.shortcuts import render, redirect
from django.db.models import Count
from django.core.cache import cache
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from home.serializers import *


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'home/home.html')


# 404 page not found

def page_not_found(request, exception=None):
    return render(request, 'home/404-page.html', status=status.HTTP_404_NOT_FOUND)


# def sign_up_required(request, exception=None):
#     return render(request, 'accounts/signup.html' ,status=status.HTTP_403_FORBIDDEN)


class AllTeacher(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = TeacherSerializer

    # return those users that are teacher

    def get_queryset(self):
        cache_get = cache.get('my_key')
        if cache_get:
            return cache_get
        else:
            queryset = User.objects.filter(role__code='3')
            cache.set('my_key', queryset, 1000)
            return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BestSellingCourses(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer

    def get_queryset(self):
        cache_get = cache.get('my_key')
        if cache_get:
            return cache_get
        # get courses those have most students
        course = Course.objects.annotate(number=Count('user'))
        # get the number of courses
        count = Course.objects.all().count()
        # if courses are few return all of them
        if count < 5:
            cache.set('my_key', course, 1000)
            return course
        # sorted courses by number of students
        course_order = course.order_by('-number')
        if count > 100:
            cache.set('my_key', course_order[:14], 1000)
            # the highest size of query for sending is 14
            return course_order[:14]
        else:
            cache.set('my_key', course_order[:4 + (count / 10)], 3600)
            # return a query that size of it suitable with count
            return course_order[:4 + (count / 10)]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MostDiscountedCourses(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer

    def get_queryset(self):
        cache_get = cache.get('my_key')
        if cache_get:
            return cache_get
        time_now = datetime.datetime.now()
        # get those discounts that the time of them reach
        discounts = Discount.objects.filter(Q(code=None) and Q(start_date__lt=time_now) and Q(end_date__gt=time_now))
        # get those courses that have discounts now
        course = Course.objects.filter(discount__in=discounts)
        cache.set('my_key', course, 1000)
        return course

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
