from django.shortcuts import render , redirect
from accounts.models import User

from .forms import ProfileForm


# Create your views here.
def dashboard(request):
    return render(request , 'dashboard/dashboard.html')


# Edit Profile Page 
def edit_profile(request):
    if request.method == 'POST':
        if request.POST.get("upload"):
            
            form = ProfileForm(data=request.POST , instance=request.user)
            if form.is_valid():
                form.save()
                return redirect ('dashboard')
        else:
            form = ProfileForm() 
            form.errors = {'username' : "خطا در ثبت نام" } 
            return render(request , 'dashboard/profile_page.html' , {'form':form})
    else:  
        form = ProfileForm()
        return render(request , 'dashboard/profile_page.html' , { 'form':form })


# Lessons Page
def lessons(request):
    return render (request , 'dashboard/lessons.html')
