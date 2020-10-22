from django.shortcuts import render, redirect
from django.db.models import Count
from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from accounts.enums import *
from home.serializers import *
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


def main_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('home')


# def home(request):
#     return render(request, 'home/home.html')


# 404 page not found

def page_not_found(request, exception=None):
    return render(request, 'home/404-page.html', status=status.HTTP_404_NOT_FOUND)


# def sign_up_required(request, exception=None):
#     return render(request, 'accounts/signup.html' ,status=status.HTTP_403_FORBIDDEN)

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


class TeacherViewset(viewsets.ModelViewSet):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = TeacherSerializer
    pagination_class = None
    lookup_field = 'username'
    queryset = User.objects.filter(role__code=RoleCodes.TEACHER.value)
    # return those users that are teacher
    http_method_names = ['get', ]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super(TeacherViewset, self).list(request)

    def retrieve(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'json':
            return super(TeacherViewset, self).retrieve(request, *args, **kwargs)
        # add template !
        # return render()
        return super(TeacherViewset, self).retrieve(request, *args, **kwargs)


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
        # this is forbidden code
        course_order = Course.objects.filter(end_date__gt=time_now).exclude(
            lesson__code=PrivateCourse.MEMBERSHIP.value).annotate(number=Count('installment__user')).order_by('-number')
        # sorted courses by number of students
        if count > 100:
            # the highest size of query for sending is 14
            return course_order[:12]
        else:
            # return a query that size of it suitable with count
            return course_order[:2 + int(count / 10)]


class MostDiscountedCourses(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseDiscountedSerializer
    pagination_class = None

    def get_queryset(self):
        # print(self.request.headers)
        time_now = datetime.datetime.now()
        # get those discounts that the time of them reach
        query = Q(start_date__lte=time_now)
        query &= Q(code__isnull=True)
        query &= (Q(end_date__gte=time_now) | Q(end_date=None))
        query &= ~(Q(courses=None))
        # this is forbidden code
        # query &= (~Q(courses__lesson__code=PrivateCourse.MEMBERSHIP.value))
        discounts = Discount.objects.filter(query)
        # get those courses that have discounts now
        # this is forbidden code
        course = Course.objects.filter(discount__in=discounts).exclude(
            lesson__code=PrivateCourse.MEMBERSHIP.value).order_by('-discount__percent',
                                                                  F('discount__end_date').asc(nulls_last=True))
        if not course.exists():
            try:
                query = Q(start_date__lte=time_now)
                query &= Q(code__isnull=True)
                query &= (Q(end_date__gte=time_now) | Q(end_date=None))
                query &= (Q(courses=None))
                Discount.objects.get(query)
                # this is forbidden code
                return Course.objects.filter(end_date__gt=time_now).exclude(
                    lesson__code=PrivateCourse.MEMBERSHIP.value).order_by('-end_date')[:12]
            except:
                return None
        return course


class NewCourseHome(generics.ListAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer
    pagination_class = None

    def get_queryset(self):
        time_now = datetime.datetime.now()
        # this is forbidden code
        return Course.objects.filter(end_date__gte=time_now).exclude(
            lesson__code=PrivateCourse.MEMBERSHIP.value).order_by('-id')[:12]


class SearchHome(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer
    pagination_class = None

    def get_queryset(self):
        # get three courses that have most similarity with courses in data base
        title = self.request.GET.get('title')
        time_now = datetime.datetime.now()
        # get those discounts that the time of them reach
        query = Q(end_date__gte=time_now)
        query &= (Q(title__icontains=title) | Q(teacher__last_name__icontains=title))
        # this is forbidden code
        query &= (~Q(lesson__code=PrivateCourse.MEMBERSHIP.value))
        course = Course.objects.filter(query).order_by('-end_date')[:3]
        return course

    def get(self, request):
        course = self.get_queryset()
        serialize = CourseSerializer(course, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)


class Support(generics.ListAPIView):
    queryset = Support.objects.filter(type_choice=Support.public)
    renderer_classes = [JSONRenderer]
    permission_classes = (AllowAny,)
    serializer_class = SupportSerializer
    pagination_class = None
