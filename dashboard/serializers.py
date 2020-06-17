from django.contrib.auth.models import User
from accounts.models import *
from rest_framework import serializers
from html_json_forms.serializers import JSONFormSerializer
from pip._vendor.pkg_resources import require
from django.contrib.auth.hashers import make_password
from accounts.serializers import *
class TeacherSerializer(JSONFormSerializer,serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_user_full_name')

    class Meta:
        model = Course
        fields = ('id','full_name')
        
    def get_user_full_name(self, obj):
        return obj.get_full_name()


class LessonSerializer(JSONFormSerializer,serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id','title')


class CourseBriefSerializer(JSONFormSerializer,serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField('get_user_full_name')

    class Meta:
        model = Course
        fields = ('teacher','title','image')
        
        
    def get_user_full_name(self, obj):
        return obj.teacher.get_full_name()
           


class CourseLessonsSerializer(CourseBriefSerializer):
    first_class=serializers.SerializerMethodField('get_first_class')
    
    def get_first_class(self, obj):
        return obj.get_first_class()
    
    class Meta:
        model = Course
        fields = ('title','start_date','end_date','code','amount','description','first_class','image','teacher')

class CourseCalendarSerializer(JSONFormSerializer,serializers.ModelSerializer):
    course=CourseBriefSerializer(read_only=True)
    class Meta:
        model = Course_Calendar
        fields = ('start_date','course')


class DashboardSerializer(serializers.Serializer):
    course_calendars=CourseCalendarSerializer(many=True)
    now = serializers.DateTimeField()
    calendar_time=serializers.DurationField(required=False,allow_null=True)
    
        
class ShoppingSerializer(serializers.Serializer):
    courses=CourseLessonsSerializer(many=True)
    teachers = TeacherSerializer(many=True)
    lessons = LessonSerializer(many=True)
    grades =  GradeSerializer(many=True)
    
    
class UserProfileSerializer(JSONFormSerializer,serializers.ModelSerializer):
    grade = serializers.SerializerMethodField('get_student_grade')
    cityTitle= serializers.SerializerMethodField('get_city_title')
    class Meta:
        model = User
        fields = ( 'first_name',
                  'last_name','username','grade','cityTitle', 'gender','national_code', 'phone_number','avatar')    
    
        
    def get_student_grade(self, obj):
        try:
            return obj.grades.all().first().title
        except:
            return ""
        
    def get_city_title(self, obj):
        try:
            return obj.city.title
        except:
            return ""    
    
#for post method and android
class UserSaveProfileSerializer(UserProfileSerializer):
    class Meta:
        model = User
        fields = ( 'first_name',
                  'last_name','username','email' ,'grade','cityTitle', 'gender', 'phone_number','national_code','grades','city','avatar')    
    
        

#for get method
class UserProfileShowSerializer(serializers.Serializer):
    user = UserProfileSerializer()
    grades =  GradeSerializer(many=True)
    cities = CitySerializer(many=True)
        
       
    
