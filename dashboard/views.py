import pytz
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
import datetime
from accounts.models import *

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
            courses = user.payments.order_by('course_calendar__end_date').distinct()
            next_course_calendar = courses[0].course_calendar_set.first()

        class_time = next_course_calendar.start_date
        is_class_active = next_course_calendar.is_class_active
    else:
        class_time = ''
        is_class_active = False
    # ------------------------------------------------------------------------------------------------------------------

    return render(request, 'dashboard/dashboard.html', {'now': now, 'courses': courses,
                                                        'class_time': class_time-now_utc,
                                                        'is_class_active':is_class_active})


# Edit Profile Page 
def edit_profile(request):
    if request.method == 'POST':
        if request.POST.get("upload"):
            avatar = request.FILES.get("avatar")
            if request.user.avatar:
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
    return render(request, 'dashboard/lessons.html')
