from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from html_json_forms.serializers import JSONFormSerializer
from pip._vendor.pkg_resources import require
from .enums import Sms
from melipayamak import Api
from django.contrib.auth.hashers import make_password
import random



class UserSerializer(JSONFormSerializer,serializers.ModelSerializer):
    password=serializers.CharField(required=False)
    grades = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), many=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(),required=False)
    class Meta:
        model = User
        fields = ('username',  'email','first_name',
                  'last_name', 'grades', 'gender', 'phone_number','password','role','city')

        
    def validate(self,data):
        try :
            data['role']
        except:
            data['role']=Role.objects.get(code=RoleCodes.STUDENT.value)
        api = Api(Sms.username.value, Sms.password.value)
        sms = api.sms()
        to = "0"+data['phone_number']
        _from = Sms._from.value
        randPass = random.randint(10000000, 99999999)
        text = Sms.signupText.value.replace('{}', str(randPass))
        response = sms.send(to, _from, text)
        if response['Value'] == Sms.wrongNumber.value:
            raise serializers.ValidationError({"phone_number":'شماره وارد شده نامعتبر است'}) 
        elif (len(response['Value']) == 1):
            raise serializers.ValidationError('خطایی رخ داده است . لطفا یک بار دیگر تلاش کنید یا با پشتیبان تماس بگیرید')
        data['password']=randPass
        return data    
        
      
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
class GradeSerializer(JSONFormSerializer,serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class CitySerializer(JSONFormSerializer,serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'      
        
class SignUpSerializer(serializers.Serializer):
    grades = GradeSerializer(many=True)
    cities = CitySerializer(many=True)     
        