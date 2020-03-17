from django.shortcuts import render , redirect
from accounts.models import User
from .forms import ProfileForm

# Create your views here.


def dashboard(request):
    return render(request , 'dashboard/dashboard.html')

# Edit Profile Page 
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST , instance=request.user)
        if form.is_valid():
            form.save()
            return redirect ('dashboard')
        else:
            form = ProfileForm() 
            return render(request , 'dashboard/profile_page.html' , {'error' : "خطا در ثبت نام" , 'form':form})
    else:  
        form = ProfileForm()  
        return render(request , 'dashboard/profile_page.html' , { 'form':form })