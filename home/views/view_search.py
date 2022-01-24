from datetime import datetime
from django.db.models import Q
from rest_framework import generics
from core.pagination import Pagination
from dashboard.models import Course
from home.serializers.serializer_course_home import CourseHomeSerializer


class SearchHomePagination(Pagination):
    page_size = 3

class SearchHome(generics.ListAPIView):
    serializer_class = CourseHomeSerializer
    pagination_class = SearchHomePagination
    queryset = Course.objects.filter(Q(is_active=True)).order_by(
        '-end_date')
    search_fields = ('title', 'teacher__last_name')

    def get_queryset(self):
        query = super(SearchHome, self).get_queryset()
        time_now = datetime.now()
        query = query.filter(Q(end_date__gte=time_now))
        return query