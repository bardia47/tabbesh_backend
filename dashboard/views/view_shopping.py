import datetime

from django.db.models import Q, Case, When, Value, IntegerField
from rest_framework import viewsets
from operator import or_
from functools import reduce
from dashboard.enums.enum_installmentmodel import InstallmentModelEnum
from dashboard.filters.filter_shopping import ShoppingFilter
from dashboard.models import Course
from dashboard.serializers.serializer_shopping_course import ShoppingCourseSerializer


class ShoppingCourseViewSet(viewsets.ReadOnlyModelViewSet):
    # thats fake :/ because its Mandatory
    queryset = Course.objects.filter(is_active=True)
    serializer_class = ShoppingCourseSerializer
    filterset_class = ShoppingFilter
    # default show all active courses
    def get_queryset(self):
        now = datetime.datetime.now()
        queryset = super(ShoppingCourseViewSet, self).get_queryset()
        query = Q(end_date__gt=now + datetime.timedelta(days=InstallmentModelEnum.installmentDateBefore.value))
        if self.request.user.is_authenticated:
            if self.request.user.courses().all():
                queryNot = reduce(or_, (Q(id=course.id)
                                        for course in self.request.user.courses().all()))
                query = query & ~queryNot
            queryset = queryset.filter(query)
            if self.request.user.grades.count() > 0:
                query1 = (Q(grades__id=self.request.user.grades.first().id) | Q(grades__id=None))
                query2 = ~(Q(grades__id=self.request.user.grades.first().id) | Q(grades__id=None))
                queryset = (queryset
                            .filter(query1 | query2).annotate(
                    search_type_ordering=Case(
                        When(query1, then=Value(2)),
                        When(query2, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()))
                            .order_by('-search_type_ordering'))
        return queryset.distinct()