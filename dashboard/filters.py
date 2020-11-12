from django_filters import rest_framework as filters
from accounts.models import Course, Lesson
from functools import reduce
from operator import or_
from django.db.models import Q


class ShoppingFilter(filters.FilterSet):
    teacher = filters.NumberFilter(field_name="teacher__id")
    lesson = filters.NumberFilter(field_name="lesson__id", method='get_all_lessons')
    grade = filters.NumberFilter(field_name="grades__id")

    def get_all_lessons(self, queryset, name, value):
        lessons = Lesson.objects.filter(id=value)
        whilelessons = lessons
        while True:
            extend_lesson = []
            query = reduce(or_, (Q(parent__id=lesson.id)
                                 for lesson in whilelessons))
            extend_lesson = Lesson.objects.filter(query)
            if len(extend_lesson) == 0:
                break
            else:
                whilelessons = extend_lesson
                lessons = lessons | whilelessons
        query = reduce(or_, (Q(lesson__id=lesson.id) for lesson in lessons))
        return queryset.filter(query)

    class Meta:
        model = Course
        fields = [ 'grade', 'lesson', 'teacher']