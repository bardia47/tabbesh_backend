from django.shortcuts import render
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request , 'dashboard/dashboard.html')
    else:
        return render(request , 'home/home.html')
        
