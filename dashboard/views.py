from django.shortcuts import render, redirect, get_object_or_404
import datetime
from accounts.models import *
from accounts.enums import RoleCodes
from django.db.models import Q
from operator import or_
from functools import reduce
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers  import *


class Dashboard(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def get(self, request):
        now = datetime.datetime.now()
        user = get_object_or_404(User, pk=request.user.id)
        courses = user.courses.filter(end_date__gt=now)
        classes = Course_Calendar.objects.filter(course__in=courses)
        classes = Course_Calendar.objects.filter(
        Q(start_date__day=now.day) | Q(start_date__day=now.day + 1), course__in=courses)
        if classes.count() > 0:
            calendar_time = classes.first().start_date - now
        else:
            calendar_time = None
        if request.accepted_renderer.format == 'html':
            return Response({'now': now, 'classes': classes, 'calendar_time': calendar_time}, template_name='dashboard/dashboard.html')
        ser = DashboardSerializer(instance={'course_calendars': classes, 'now': now, 'calendar_time': calendar_time})
        return Response(ser.data)
        

# Edit Profile Page
class EditProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def get(self, request):
        form = ProfileForm()
        if request.accepted_renderer.format == 'html':
            return render(request, 'dashboard/profile_page.html', {'form': form})
        ser = UserProfileSerializer(request.user)
        return Response(ser.data)


# Edit profile page --> change avatar form
@login_required
def change_avatar(request):
    if request.method == 'POST':
        form = ProfileForm()
        avatar = request.user.compressImage(request.FILES.get("file"))
        if avatar:
            if not request.user.avatar.url.startswith("/media/defaults"):
                request.user.avatar.delete()
            request.user.avatar = avatar
            request.user.save()
        return redirect('dashboard')
    else:
        error = 'تغییر پروفایل با مشکل رو به رو شد'
        return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})


# Edit profile page --> change field except avatar field
@login_required
def change_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'dashboard/profile_page.html', {'form': form})


# Edit profile page --> change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ProfileForm()
        if not request.user.check_password(request.POST['old_password']):
            error = 'رمز وارد شده اشتباه است'
            return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})
        else:
            error = 'تغییر رمز با موفقیت انجام شد'
            request.user.password = make_password(request.POST['password'])
            request.user.save()
            return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})


# Lessons Page
class Lessons(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        now = datetime.datetime.now()
        if request.accepted_renderer.format == 'html':
            return Response({"have_class" : request.user.courses.filter(end_date__gt=now).count()!=0} ,template_name='dashboard/lessons.html')
# Shopping Page
class Shopping(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    def get(self, request):
        grades = Grade.objects.all()
        lessons = Lesson.objects.all()
        teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        ser = ShoppingSerializer(instance={'grades': grades, 'lessons': lessons, 'teachers': teachers})
        return Response(ser.data, template_name='dashboard/shopping.html')


def getAllLessons(lesson_id, now):
    lessons = Lesson.objects.filter(id=lesson_id)
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
    return query


# File manager page
@login_required
def filemanager(request, code):
    course = Course.objects.get(code=code)
    try:
        request.user.courses.get(id=course.id)
    except:
        return shopping(request)
    documents = course.document_set.all()
    return render(request, 'dashboard/filemanager.html', {'course': course, 'documents': documents})


class GetLessonsViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseLessonsSerializer
    http_method_names = ['get',]

    search_fields = ('title',)
    ordering_fields =  ('title', )
    
    def get_queryset(self):
         now = datetime.datetime.now()
         user = get_object_or_404(User, pk=self.request.user.id)
         courses = user.courses.filter(end_date__gt=now)
         return courses


class GetShoppingViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = ShoppingCourseSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        now = datetime.datetime.now()
        query = Q(end_date__gt=now)
        if self.request.GET.get("teacher") or self.request.GET.get("lesson") or self.request.GET.get("grade"):
            if self.request.GET.get("lesson"):
                query &= getAllLessons(self.request.GET.get("lesson"), now)
            if self.request.GET.get("grade"):
                query &= Q(grade__id=self.request.GET.get("grade"))
            if self.request.GET.get("teacher"):
                query &= Q(teacher__id=self.request.GET.get("teacher"))
        else:
            if (self.request.user.grades.count() > 0):
                query &= Q(grade__id=self.request.user.grades.first().id)

        if self.request.user.courses.all():
            queryNot = reduce(or_, (Q(id=course.id)
                                    for course in self.request.user.courses.all()))
            query = query & ~queryNot
        courses = Course.objects.filter(query)
        return courses