from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Picture Models
class Picture(models.Model):
    id = models.IntegerField(primary_key = True)
    picture = models.ImageField()


# Role Models
class Role(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length= 30)

# Profile Models
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key = True ,  on_delete=models.CASCADE)
    picture_id = models.ForeignKey(Picture , on_delete = models.SET_NULL , null =True , blank=True)
    gender = models.BooleanField (blank=True)
    biography = models.CharField(max_length = 255 , blank=True)
    role_id = models.ForeignKey(Role , on_delete = models.SET_NULL , null =True , blank=True)
    national_code = models.CharField(max_length = 10 , blank=True)
    address = models.CharField(max_length=255 , blank=True) 


#Grade Models

class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)

# Relational Model Between Profiles & Grades
class User_grade_relation(models.Model):
    id = models.IntegerField(primary_key = True)
    user_id = models.ForeignKey(Profile , on_delete = models.SET_NULL , null = True)
    grade_id = models.ForeignKey(Grade , on_delete = models.SET_NULL , null = True)
    unique_together = [['user_id', 'grade_id']]




