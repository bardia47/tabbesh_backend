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
    next_course_calendar = courses[0].course_calendar_set.first()
    if next_course_calendar.end_date < now_utc:
        next_course_calendar.end_date += datetime.timedelta(days=7)
        next_course_calendar.save()
        next_course_calendar.start_date += datetime.timedelta(days=7)
        next_course_calendar.save()
        courses = user.payments.order_by('course_calendar__end_date').distinct()
        next_course_calendar = courses[0].course_calendar_set.first()

    calendar_time = next_course_calendar.start_date - now_utc
    calendar_time_total_seconds = calendar_time.seconds
    calendar_day = calendar_time.days
    calendar_second = divmod(calendar_time_total_seconds, 60)[1]
    calendar_time_total_minutes = divmod(calendar_time_total_seconds, 60)[0]
    calendar_hour = divmod(calendar_time_total_minutes, 60)[0]
    calendar_minute = divmod(calendar_time_total_minutes, 60)[1]
    if calendar_day < 0:
        calendar_day = 0
        calendar_hour = 0
        calendar_minute = 0
        calendar_second = 0

    is_class_active = next_course_calendar.is_class_active
    # ------------------------------------------------------------------------------------------------------------------

    return render(request, 'dashboard/dashboard.html', {'now': now, 'courses': courses,
                                                        'calendar_day': calendar_day,
                                                        'calendar_hour': calendar_hour,
                                                        'calendar_minute': calendar_minute,
                                                        'calendar_second': calendar_second,
                                                        'is_class_active': is_class_active})


# Edit Profile Page 
def edit_profile(request):
    if request.method == 'POST':
        if (request.POST.get("upload")):
           avatar= request.FILES.get("avatar")
           if (request.user.avatar):
               request.user.avatar.delete()
           request.user.avatar=avatar
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
