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
from .serializers  import *


class Dashboard(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def get(self, request):
        now = datetime.datetime.now()
        user = get_object_or_404(User, pk=request.user.id)
        courses = user.courses.filter(end_date__gt=now)
        classes = Course_Calendar.objects.filter(course__in=courses)

        # update all classes time
        for klass in classes:
            while klass.end_date < now:
                klass.start_date += datetime.timedelta(days=7)
                klass.end_date += datetime.timedelta(days=7)
                klass.save()
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
@login_required
def edit_profile(request):
    form = ProfileForm()
    return render(request, 'dashboard/profile_page.html', {'form': form})


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
            form = ProfileForm()
            return render(request, 'dashboard/profile_page.html', {'form': form, 'error': 'خطا در ثبت نام'})


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
        user = get_object_or_404(User, pk=request.user.id)
        courses = user.courses.filter(end_date__gt=now)
        classes = Course_Calendar.objects.filter(course__in=courses)
        # update all classes time
        for klass in classes:
            while klass.end_date < now:
                klass.start_date += datetime.timedelta(days=7)
                klass.end_date += datetime.timedelta(days=7)
                klass.save()
        if request.accepted_renderer.format == 'html':
            return Response({'courses': courses} , template_name='dashboard/lessons.html')
        ser = CourseLessonsSerializer(instance=courses, many=True)
        return Response(ser.data)    


# Shopping Page
class Shopping(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    def get(self, request):
        now = datetime.datetime.now()
        grades = Grade.objects.all()
        lessons = Lesson.objects.all()
        teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        query = Q(end_date__gt=now)
        if request.GET.get("teacher") or request.GET.get("lesson") or request.GET.get("grade"):
            if request.GET.get("lesson"):
                query &= getAllLessons(request.GET.get("lesson"), now)
            if request.GET.get("grade"):
                query &= Q(grade__id=request.GET.get("grade"))
            if request.GET.get("teacher"):
                query &= Q(teacher__id=request.GET.get("teacher"))
        else:
            if (request.user.grades.count() > 0):
                query &= Q(grade__id=request.user.grades.first().id)
            if request.user.courses.all():
                queryNot = reduce(or_, (Q(id=course.id)
                                for course in request.user.courses.all()))
                query = query & ~queryNot
        courses = Course.objects.filter(query)
        if request.accepted_renderer.format == 'html':
            return Response({'grades': grades, 'lessons': lessons, 'teachers': teachers, 'courses': courses}, template_name='dashboard/shopping.html')  
        ser = ShoppingSerializer(instance={'grades': grades, 'lessons': lessons, 'teachers': teachers, 'courses': courses})
        return Response(ser.data)  


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
