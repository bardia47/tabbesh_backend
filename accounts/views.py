from django.shortcuts import render, redirect
from django.contrib import auth
from accounts.models import *
from accounts.serializers import *
from rest_framework.parsers import JSONParser
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from zeep.xsd.elements import element
# Create your views here.


@permission_classes((AllowAny,))
class SignUp(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def get(self, request):
        grades = Grade.objects.all()
        if request.accepted_renderer.format == 'html':
            return Response({'grades' : grades}, template_name='accounts/signup.html')        
        grades = GradeSerializer(instance=grades, many=True)
        return Response(grades.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        grades = Grade.objects.all()
        if not serializer.is_valid():
            if request.accepted_renderer.format == 'html':
                return Response({'serializer': serializer, 'grades' : grades}, template_name='accounts/signup.html')
            return Response(serializer.errors)
        serializer.save()
        if request.accepted_renderer.format == 'html':
             return render(request, 'accounts/signin.html', {'signup_success': 'ثبت نام با موفقیت انجام شد.'}) 
        return Response({'signup_success': 'ثبت نام با موفقیت انجام شد.'})
 
        


@permission_classes((AllowAny,))
class SignIn(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def get(self, request):
        if request.accepted_renderer.format == 'html':
            return render(request, 'accounts/signin.html')
    
    def post(self, request):
        if request.POST['username'].isdigit():
            try:
                user1 = User.objects.get(phone_number=request.POST['username'])
            except User.DoesNotExist:
                return render(request, 'accounts/signin.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
            user = auth.authenticate(
                username=user1.username, password=request.POST['password'])
        else:
            user = auth.authenticate(
                username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/signin.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})


def signout(request):
    auth.logout(request)
    return redirect('home')
