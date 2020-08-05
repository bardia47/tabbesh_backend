from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'home/home.html')

# 404 page not found

def page_not_found(request, exception=None):
        return render(request, 'home/404-page.html' ,status=status.HTTP_404_NOT_FOUND)


def sign_up_required(request, exception=None):
    return render(request, 'accounts/signup.html' ,status=status.HTTP_403_FORBIDDEN)
