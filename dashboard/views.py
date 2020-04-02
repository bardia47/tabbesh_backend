from django.shortcuts import render, redirect, get_object_or_404
import datetime
from accounts.models import *
from accounts.enums import RoleCodes
from django.db.models import Q
from operator import or_
from functools import reduce

from .forms import ProfileForm


def dashboard(request):
    now = datetime.datetime.now()
    # courses and down counter(for the next course)
    user = get_object_or_404(User, pk=request.user.id)
    courses = user.payments.order_by('course_calendar').filter(end_date__gt=now)
    classes = Course_Calendar.objects.filter(course__in=courses, start_date__day=now.day)
    no_class_today_text = None

    if classes.count() > 0:
        next_class = classes.first()
        if next_class.end_date < now:
            next_class.end_date += datetime.timedelta(days=7)
            next_class.start_date += datetime.timedelta(days=7)
            next_class.save()
            classes = Course_Calendar.objects.filter(course__in=courses, start_date__day=now.day)
            next_class = classes.first()
        calendar_time = next_class.start_date - now
    else:
        calendar_time = ''
        no_class_today_text = 'امروز هیچ کلاسی نداری'

    return render(request, 'dashboard/dashboard.html', {'now': now, 'classes': classes,
                                                        'calendar_time': calendar_time,
                                                        'no_class_today_text': no_class_today_text})


# Edit Profile Page
def edit_profile(request):
    if request.method == 'POST':
        if request.POST.get("upload"):
            avatar = request.user.compressImage(request.FILES.get("file"))
            if avatar:
                if not request.user.avatar.url.startswith("/media/defaults"):
                    request.user.avatar.delete()
                request.user.avatar = avatar
                request.user.save()
            return redirect('dashboard')

        else:
            form = ProfileForm(data=request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
            else:
                form = ProfileForm()
                return render(request, 'dashboard/profile_page.html', {'form': form, 'error': 'خطا در ثبت نام'})
    else:
        form = ProfileForm()
        return render(request, 'dashboard/profile_page.html', {'form': form})


# Lessons Page
def lessons(request):
    now = datetime.datetime.now()
    user = get_object_or_404(User, pk=request.user.id)
    courses = user.payments.filter(end_date__gt=now)
    return render(request, 'dashboard/lessons.html', {'courses': courses})


# Shopping Page
def shopping(request):
    now = datetime.datetime.now()
    grades = Grade.objects.all()
    lessons = Lesson.objects.all()
    teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
    if request.GET.get("teacher") or request.GET.get("lesson") or request.GET.get("grade"):
        if request.GET.get("lesson"):
            courses = getAllLessons(request.GET.get("lesson"),now)
        else:
            courses = Course.objects.filter(end_date__gt=now)    
        if request.GET.get("grade"):
            courses = courses.filter(grade__id=request.GET.get("grade"))
        if request.GET.get("teacher"):
            courses = courses.filter(teacher__id=request.GET.get("teacher"))               
    else:  
        courses = Course.objects.filter(end_date__gt=now)  
        if (request.user.grades.count() > 0):
                courses = courses.filter(grade__id=request.user.grades.first().id)
           
            
            
    

    return render(request, 'dashboard/shopping.html', {'grades': grades, 'lessons': lessons, 'teachers': teachers,
                                                       'courses': courses})
    
def getAllLessons(lesson_id,now):
    lessons = Lesson.objects.filter(id=lesson_id) 
    whilelessons=lessons
    while True:
        extend_lesson=[]
        query = reduce(or_, (Q(parent__id=lesson.id) for lesson in whilelessons))
        extend_lesson=Lesson.objects.filter(query)
        if  len(extend_lesson)==0 :
            break 
        else:
            whilelessons=extend_lesson
            lessons.extened(whilelessons)
    query = reduce(or_, (Q(lesson__id=lesson.id) for lesson in lessons))
    courses = Course.objects.filter(query | Q(end_date__gt=now)) 
    return courses

    
