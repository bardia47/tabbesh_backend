from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from accounts.forms import UserForm
from accounts.models import City


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                form = UserForm()
                form.errors = {'username': 'please try another username'}
                return render(request, 'accounts/signup.html', {'form': form})
            except User.DoesNotExist:
                # city = City.objects.get(id=request.POST['city'])
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password'])
                auth.login(request, user)
                return redirect('edit_profile')
        else:
            form.errors = {'password': 'Passwords must match'}
            return render(request, {'form': form})
    else:
        form = UserForm()
        return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        if '@' in request.POST['username']:
            user = auth.authenticate(email=request.POST['username'], password=request.POST['password'])
        else:
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/signin.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
    else:
        return render(request, 'accounts/signin.html')


def signout(request):
    auth.logout(request)
    return redirect('home')
