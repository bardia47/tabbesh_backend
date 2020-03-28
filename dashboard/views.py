import pytz
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
import datetime
from accounts.models import *
from accounts.enums import RoleCodes

from .forms import ProfileForm


# Create your views here.
def dashboard(request):
    # just for calendar
    now = datetime.datetime.now()

    # courses and downcounter(for the next course) ---------------------------------------------------------------------
    now_utc = datetime.datetime.now(pytz.utc)
    user = get_object_or_404(User, pk=request.user.id)
    courses = user.payments.order_by('course_calendar__end_date').distinct()
    if courses.count() > 0:
        next_course_calendar = courses[0].course_calendar_set.first()
        if next_course_calendar.end_date < now_utc:
            next_course_calendar.end_date += datetime.timedelta(days=7)
            next_course_calendar.start_date += datetime.timedelta(days=7)
            next_course_calendar.save()
            courses = user.payments.order_by(
                'course_calendar__end_date').distinct()
            next_course_calendar = courses[0].course_calendar_set.first()

        class_time = next_course_calendar.start_date
        is_class_active = next_course_calendar.is_class_active
        class_time = class_time - now_utc
    else:
        class_time = ''
        is_class_active = False
    # ------------------------------------------------------------------------------------------------------------------

    return render(request, 'dashboard/dashboard.html', {'now': now, 'courses': courses,
                                                        'class_time': class_time,
                                                        'is_class_active': is_class_active})


# Edit Profile Page
def edit_profile(request):
    if request.method == 'POST':
        if request.POST.get("upload"):
            avatar = request.FILES.get("avatar")
            if  avatar  :
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
    user = get_object_or_404(User, pk=request.user.id)
    courses = user.payments.all()
    return render(request, 'dashboard/lessons.html', {'courses': courses})


# Shopping Page
def shopping(request):
    grades = Grade.objects.all()
    LESSONS = Lesson.objects.all()
    teachers = User.objects.filter(role__code=RoleCodes.TEACHER.value)
    courses = Course.objects.all()
    if request.GET.get("teacher") or request.GET.get("lesson") or request.GET.get("grade"):
        if request.GET.get("teacher"):
            courses = courses.filter(teacher__id=request.GET.get("teacher"))
        if request.GET.get("grade"):
            courses = courses.filter(lesson__grade__id=request.GET.get("grade"))
        if request.GET.get("lesson"):
            courses = courses.filter(lesson__id=request.GET.get("lesson"))

    return render(request, 'dashboard/shopping.html', {'grades': grades, 'lessons': LESSONS, 'teachers': teachers,
                                                       'courses': courses})
