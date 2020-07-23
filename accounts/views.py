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
from rest_framework.decorators import  permission_classes
from zeep.xsd.elements import element
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@permission_classes((AllowAny,))
class SignUp(APIView):
    # change default browsable api render to templatehtml render
    # and also you need add json
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def get(self, request):
        grades = Grade.objects.all()
        cities = City.objects.all()
        if request.accepted_renderer.format == 'html':
            return Response({'grades' : grades ,'city' : cities}, template_name='accounts/signup.html')        
        serializer = SignUpSerializer(instance={'grades': grades, 'cities': cities})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
             if request.accepted_renderer.format == 'html':
                grades = Grade.objects.all()
                cities = City.objects.all()
                return Response({'serializer': serializer, 'grades' : grades ,'city' : cities ,'grades0' : request.data['grades[0]']}, template_name='accounts/signup.html')
             return Response(serializer.errors , status=status.HTTP_406_NOT_ACCEPTABLE)
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
        return Response({},status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request):
        if request.data['username'].isdigit():
            try:
                user1 = User.objects.get(phone_number=request.data['username'])
            except User.DoesNotExist:
                return render(request, 'accounts/signin.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
            user = auth.authenticate(
                username=user1.username, password=request.data['password'])
        else:
            user = auth.authenticate(
                username=request.data['username'], password=request.data['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/signin.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
 
@permission_classes((AllowAny,)) 
class MyTokenObtainPairSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        try:
            if attrs.get('username').isdigit():
                try:
                    user1 = User.objects.get(phone_number=attrs.get('username'))
                except User.DoesNotExist:
                        raise exceptions.AuthenticationFailed("error", "authentication field")
                attrs['username']=user1.username
        finally:
            return super().validate(attrs)


class MyTokenObtainPairView(ObtainAuthToken):
    serializer_class = MyTokenObtainPairSerializer

 
 
       

class SignOut(APIView):
    def get(self, request):
        if request.accepted_renderer.format == 'json':
            try:
                request.user.auth_token.delete()
            except (AttributeError, ObjectDoesNotExist):
                pass
            return Response(status=status.HTTP_200_OK)
        auth.logout(request)
        return redirect('home')
        
