from django.shortcuts import render, redirect
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request , 'home/home.html')
        
