from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from accounts.forms import UserForm
from accounts.models import City
from django.db.models import Q
from melipayamak import Api
from .enums import Sms
import random 
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.gender=request.POST['gender']
        user = User.objects.filter(Q(username=form.data['username']) | Q(phone_number=form.data['phone_number']))
        if user.exists():
                form.error='نام کاربری یا شماره همراه در سیستم استفاده شده و قابل تکرار نمیباشد'
                return render(request, 'accounts/signup.html', {'form': form})
        if form.is_valid():
                api = Api(Sms.username.value,Sms.password.value)
                sms = api.sms()
                to = "0"+form.data['phone_number']
                _from = '50001060690571'
                randPass = random.randint(1000, 9999) 
                text = Sms.signupText.value.replace('{}',str(randPass))
                response = sms.send(to,_from,text)
                print(response)
                if  response['Value']==Sms.wrongNumber.value:
                    form.error = 'شماره وارد شده نامعتبر است'
                elif (len(response['Value'])==1):
                    form.error = 'خطایی رخ داده است . لطفا یک بار دیگر تلاش کنید یا با پشتیبان تماس بگیرید'
                else:
                    user = User.objects.create_form_user(form,randPass) 
                    return render(request, 'accounts/signin.html', {'error': 'لطفا رمز خود را با توجه به sms ارسالی وارد کنید'})
        else:
                form.error = 'تمامی فیلد ها پر نشده اند'
        return render(request,'accounts/signup.html', {'form': form})

    else:
        form = UserForm()
        return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        if request.POST['username'].isdigit():
            try:
                user1=User.objects.get(phone_number=request.POST['username'])
            except User.DoesNotExist:
              return render(request, 'accounts/signin.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})  
            user = auth.authenticate(username=user1.username, password=request.POST['password'])
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
