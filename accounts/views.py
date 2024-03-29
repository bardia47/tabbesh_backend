from django.shortcuts import render, redirect
from django.contrib import auth
from accounts.models import *
from accounts.serializers import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password
from django.urls import reverse


# Create your views here.


@permission_classes((AllowAny,))
class SignUp(APIView):
    # change default browsable api render to templatehtml render
    # and also you need add json
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        grades = Grade.objects.all()
        cities = City.objects.all()
        if request.accepted_renderer.format == 'html':
            return Response({'grades': grades, 'city': cities}, template_name='accounts/signup.html')
        serializer = SignUpSerializer(instance={'grades': grades, 'cities': cities})
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            if request.accepted_renderer.format == 'html':
                grades = Grade.objects.all()
                cities = City.objects.all()
                return Response(
                    {'serializer': serializer, 'grades': grades, 'city': cities, 'grades0': request.data['grades[0]']},
                    template_name='accounts/signup.html')
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save()
        if request.accepted_renderer.format == 'html':
            request.session['new_login'] = True
            return render(request, 'accounts/signin.html', {'success': 'ثبت نام با موفقیت انجام شد.'})
        return Response({'success': 'ثبت نام با موفقیت انجام شد.'})


@permission_classes((AllowAny,))
class SignIn(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'accounts/signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return Response();

    def post(self, request):
        if request.data['username'].isdigit():
            try:
                username = User.objects.get(phone_number=request.data['username']).username.lower()
            except User.DoesNotExist:
                return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'})
        else:
            username = request.data['username'].lower()
        user = auth.authenticate(
            username=username, password=request.data['password'])
        if user is not None:
            auth.login(request, user)
            if request.session.get('new_login') is not None:
                return redirect('{}#changePassword'.format(reverse('profile')))
            elif request.GET.get('next') is None:
                return redirect('dashboard')
            else:
                return redirect(request.META['QUERY_STRING'].replace('next=', ''))
        else:
            return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'})


@permission_classes((AllowAny,))
class MyTokenObtainPairSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        try:
            if attrs.get('username').isdigit():
                try:
                    user1 = User.objects.get(phone_number=attrs.get('username'))
                except User.DoesNotExist:
                    raise exceptions.AuthenticationFailed("error", "authentication field")
                attrs['username'] = user1.username
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


# this is not being used
@permission_classes((AllowAny,))
class ForgetPassword(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def post(self, request):
        error = None
        try:
            user1 = User.objects.get(phone_number=request.data['phone_number'])
            to = "0" + request.data['phone_number']
            randPass = random.randint(10000000, 99999999)
            text = str(randPass)
            sendSms = SmsWebServices.send_sms(to, text, Sms.signupBodyId.value)
            if sendSms is not None:
                error = sendSms
        except User.DoesNotExist:
            error = 'شماره تلفن وارد شده در سامانه موجود نمیباشد'

        if error is not None:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST, template_name='accounts/signin.html')
        else:
            user1.password = make_password(randPass)
            user1.save()
            return Response({'success': 'ارسال با موفقیت انجام شد'}, template_name='accounts/signin.html')
