from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'home/home.html')

# 404 page not found


def page_not_found(request):
    return render(request, 'home/404-page.html')
