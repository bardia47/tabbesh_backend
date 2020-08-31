from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from html_json_forms.serializers import JSONFormSerializer
from .enums import Sms
from .webServices import SmsWebServices

from pip._vendor.pkg_resources import require

from django.contrib.auth.hashers import make_password
import random


class UserSerializer(JSONFormSerializer, serializers.ModelSerializer):
    #introducer is extra field
    introducer = serializers.CharField(max_length=12,write_only=True,required=False,allow_blank=True,allow_null=True)
    password = serializers.CharField(required=False)
    grades = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), many=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'grades', 'gender', 'phone_number', 'password', 'role', 'city','introducer')

    def validate_username(self, value):
        user = User.objects.filter(Q(username=value.lower()))
        if user.exists():
            raise serializers.ValidationError('کاربر با این نام کاربری از قبل موجود است.')
        return value.lower()

    def validate_introducer(self,value):
        if value and value !='':
            if value.startswith('0'):
                value=value[1:]
            try:
                user = User.objects.get(phone_number=value)
            except:
                raise serializers.ValidationError('شماره معرف در سامانه موجود نمیباشد')
        return value

    def validate(self, data):
        try:
            data['role']
        except:
            data['role'] = Role.objects.get(code=RoleCodes.STUDENT.value)
        if data['phone_number'].startswith('0'):
            data['phone_number']=data['phone_number'][1:]
        to = "0" + data['phone_number']
        randPass = random.randint(10000000, 99999999)
        #  text = Sms.signupText.value.replace('{}', str(randPass))
        text = str(randPass)
        # sendSms=SmsWebServices.send_sms(to,text)
        sendSms = SmsWebServices.send_sms(to, text, Sms.signupBodyId.value)

        if sendSms is not None:
            raise serializers.ValidationError({"phone_number": sendSms})
        data['password'] = randPass
        return data

    def create(self, validated_data):
        if validated_data['introducer'] and validated_data['introducer'] !='':
            introducer=validated_data['introducer']
        else:
            introducer = None

        validated_data.pop('introducer', None)
        user= User.objects.create_user(**validated_data)
        if introducer:
            related_user = User.objects.get(phone_number=introducer)
            event = Event.objects.create(user=user,type=Event.Introducing,related_user=related_user )
        return user

class GradeSerializer(JSONFormSerializer, serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class CitySerializer(JSONFormSerializer, serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class SignUpSerializer(serializers.Serializer):
    grades = GradeSerializer(many=True)
    cities = CitySerializer(many=True)
