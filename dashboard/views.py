from django.shortcuts import render, redirect, get_object_or_404
import datetime
from accounts.models import *
from accounts.enums import RoleCodes
from django.db.models import Q
from operator import or_
from functools import reduce
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


# Create your views here.
@login_required
def dashboard(request):
    now = datetime.datetime.now()
    user = get_object_or_404(User, pk=request.user.id)
    courses = user.payments.filter(end_date__gt=now)
    classes = Course_Calendar.objects.filter(course__in=courses)
    no_class_today_text = None

    # update all classes time
    for klass in classes:
        while klass.end_date < now:
            klass.start_date += datetime.timedelta(days=7)
            klass.end_date += datetime.timedelta(days=7)
            klass.save()

    classes = Course_Calendar.objects.filter(course__in=courses, start_date__day=now.day)

    if classes.count() > 0:
        calendar_time = classes.first().start_date - now
    else:
        calendar_time = ''
        no_class_today_text = True

    return render(request, 'dashboard/dashboard.html', {'now': now, 'classes': classes,
                                                        'calendar_time': calendar_time,
                                                        'no_class_today_text': no_class_today_text})


# Edit Profile Page
@login_required
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
        elif request.POST.get("changePassword"):
            form = ProfileForm()
            if not request.user.check_password("old_password"):
                error='رمز وارد شده اشتباه است'
            else:
                error='تغییر رمز با موفقیت انجام شد'

                return render(request, 'dashboard/profile_page.html', {'form': form, 'error': error})
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
@login_required
def lessons(request):
    now = datetime.datetime.now()
    user = get_object_or_404(User, pk=request.user.id)
    courses = user.payments.filter(end_date__gt=now)
    classes = Course_Calendar.objects.filter(course__in=courses)
    # update all classes time
    for klass in classes:
        while klass.end_date < now:
            klass.start_date += datetime.timedelta(days=7)
            klass.end_date += datetime.timedelta(days=7)
            klass.save()
    return render(request, 'dashboard/lessons.html', {'courses': courses})


# Shopping Page
@login_required
def shopping(request):
    now = datetime.datetime.now()
    grades = Grade.objects.all()
    lessons = Lesson.objects.all()
    teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
    query = Q(end_date__gt=now)
    if request.GET.get("teacher") or request.GET.get("lesson") or request.GET.get("grade"):
        if request.GET.get("lesson"):
          query &= getAllLessons(request.GET.get("lesson"),now)
        if request.GET.get("grade"):
             query &=Q(grade__id=request.GET.get("grade"))
        if request.GET.get("teacher"):
            query &=Q(teacher__id=request.GET.get("teacher"))               
    else:  
        if (request.user.grades.count() > 0):
               query &=Q(grade__id=request.user.grades.first().id)
    if request.user.payments.all() :
      queryNot = reduce(or_, (Q(id=course.id) for course in request.user.payments.all()))
      query=query & ~queryNot
                   
               
    courses=Course.objects.filter(query)           

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
            lessons= lessons | whilelessons
    query = reduce(or_, (Q(lesson__id=lesson.id) for lesson in lessons))
    return query

# File manager page 
@login_required
def filemanager(request,code):
    course = Course.objects.get(code=code) 
    documents=course.document_set.all()
    return render(request,'dashboard/filemanager.html',{'course': course, 'documents': documents})

    
