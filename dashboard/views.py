from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
import datetime

from .forms import ProfileForm


# Create your views here.
def dashboard(request):
    today = datetime.datetime.now()
    # user = get_object_or_404(User, pk=request.user.id)
    return render(request, 'dashboard/dashboard.html', {'today': today})


# Edit Profile Page 
def edit_profile(request):
    if request.method == 'POST':
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
