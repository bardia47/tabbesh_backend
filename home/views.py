from django.shortcuts import render, redirect
from django.db.models import Count
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from accounts.enums import *
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

# TODO:should fix url and template_name after adding correct file
class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(template_name='home/home.html')


class Counter(APIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)

    def get(self, request):
        course_counter = Course.objects.all().count()
        student_counter = User.objects.filter(role__code=RoleCodes.STUDENT.value).count()
        teacher_counter = User.objects.filter(role__code=RoleCodes.TEACHER.value).count()
        data = {"course_counter": course_counter, "student_counter": student_counter,
                "teacher_counter": teacher_counter}
        return Response(data)


class AllTeacher(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = TeacherSerializer
    pagination_class = None

    # return those users that are teacher
    def get_queryset(self):
        # cache_get = cache.get('my_key')
        # if cache_get:
        #     return cache_get
        # else:
        queryset = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        # cache.set('my_key', queryset, 1000)
        return queryset


class BestSellingCourses(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer
    pagination_class = None

    def get_queryset(self):
        time_now = datetime.datetime.now()
        # get the number of courses
        count = Course.objects.all().count()
        # if courses are few return all of them
        course_order = Course.objects.filter(end_date__gt=time_now).annotate(number=Count('user')).order_by('-number')
        # sorted courses by number of students
        if count > 100:
            # the highest size of query for sending is 14
            return course_order[:14]
        else:
            # return a query that size of it suitable with count
            return course_order[:4 + (count / 10)]


class MostDiscountedCourses(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseDiscountedSerializer
    pagination_class = None

    def get_queryset(self):
        time_now = datetime.datetime.now()
        # get those discounts that the time of them reach
        query = Q(start_date__lte=time_now)
        query &= Q(code__isnull=True)
        query &= (Q(end_date__gte=time_now) | Q(end_date=None))
        query &= ~(Q(courses=None))
        discounts = Discount.objects.filter(query)
        # get those courses that have discounts now
        course = Course.objects.filter(discount__in=discounts).order_by('-discount__percent', F('discount__end_date').asc(nulls_last=True))
        if not course.exists():
            try:
                query = Q(start_date__lte=time_now)
                query &= Q(code__isnull=True)
                query &= (Q(end_date__gte=time_now) | Q(end_date=None))
                query &= (Q(courses=None))
                Discount.objects.get(query)
                return Course.objects.filter(end_date__gt=time_now).order_by('-end_date', '-amount')[:10]
            except:
                return None
        return course


class SearchHome(APIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer
    pagination_class = None

    def get_queryset(self):
        # get three courses that have most similarity with courses in data base
        title = self.request.data['title']
        time_now = datetime.datetime.now()
        # get those discounts that the time of them reach
        query = Q(end_date__gte=time_now)
        query &= (Q(title__icontains=title) | Q(teacher__last_name__icontains=title))
        course = Course.objects.filter(query).order_by('-end_date')[:3]
        return course

    def post(self, request):
        course = self.get_queryset()
        serialize = CourseSerializer(course, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)


class Support(generics.ListAPIView):
    queryset = Support.objects.filter(type_choice=Support.public)
    renderer_classes = [JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = SupportSerializer
    pagination_class = None
