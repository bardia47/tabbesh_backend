from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from accounts.forms import UserForm
from accounts.models import City


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.gender=request.POST['gender']
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.get(username=form.data['username'])
                form = UserForm()
                form.error='نام کاربری در سیستم استفاده شده و قابل تکرار نمیباشد'
                return render(request, 'accounts/signup.html', {'form': form})
            except User.DoesNotExist:
                if form.is_valid():
                    user = User.objects.create_form_user(form)
                    auth.login(request, user)
                else:
                    form.error = 'تمامی فیلد ها پر نشده اند'
                    return render(request,'accounts/signup.html', {'form': form})
                return redirect('edit_profile')
        else:
            form.error =  'تکرار رمز صحیح نمیباشد '
            return render(request, 'accounts/signup.html', {'form': form})
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
