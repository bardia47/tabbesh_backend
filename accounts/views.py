from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == 'POST':
        if '@' in request.POST['username']:
            user = auth.authenticate(email=request.POST['username'],password=request.POST['password'])
        else:
            user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/signin.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'accounts/signin.html')

def signout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
