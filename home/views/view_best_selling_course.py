from datetime import datetime

from django.db.models import Count
from rest_framework import generics

from dashboard.models import Course
from home.serializers.serializer_course_home import CourseHomeSerializer


class BestSellingCourses(generics.ListAPIView):
    serializer_class = CourseHomeSerializer
    pagination_class = None

    def get_queryset(self):
        time_now = datetime.datetime.now()
        # get the number of courses
        count = Course.objects.all().count()
        # if courses are few return all of them
        # this is forbidden code
        course_order = Course.objects.filter(end_date__gt=time_now, is_active=True).annotate(number=Count('installment__user')).order_by('-number')
        # sorted courses by number of students
        if count > 100:
            # the highest size of query for sending is 14
            return course_order[:12]
        else:
            # return a query that size of it suitable with count
            return course_order[:2 + int(count / 10)]