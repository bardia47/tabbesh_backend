from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profiles(models.Model):
    id = models.IntegerField(primary_key= True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture_id = models.URLField()
    gender = models.BooleanField ()
    biography = models.TextField()
    role_id = models.ForeignKey('Roles',on_delete=models.DO_NOTHING)
    national_code = models.CharField(max_length=10,)
    address = models.CharField(max_length=255)

# Roles Model
class Roles(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)

# Profile Models
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key = True ,  on_delete=models.CASCADE)
    picture_id = models.ForeignKey('Picture' , on_delete = models.SET_NULL , null =True , blank=True)
    gender = models.BooleanField (blank=True)
    biography = models.CharField(max_length = 255 , blank=True)
    role_id = models.ForeignKey('Role' , on_delete = models.SET_NULL , null =True , blank=True)
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
    user_id = models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    grade_id = models.ForeignKey('Grades',on_delete=models.DO_NOTHING)
    unique_together = [['user_id', 'grade_id']]

# Grade Model
class Grades(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)


# Lesson Model
class Lessons(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)
    grade_id = models.ForeignKey('Grades' ,on_delete=models.DO_NOTHING)
    lesson_id=models.ForeignKey('Lessons' ,on_delete=models.DO_NOTHING)
    unique_together = [['title', 'grade_id']]


# Course Model
class Courses(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)
    lesson_id=models.ForeignKey('Lessons' ,on_delete=models.DO_NOTHING)
    teacher_id=models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    start_date=models.DateField
    end_date=models.DateField
    amount=models.FloatField
    url=models.URLField

# Course_Calendar Model
class Course_Calendar(models.Model):
    id = models.IntegerField(primary_key = True)
    course_id=models.ForeignKey('Courses' ,on_delete=models.DO_NOTHING)
    start_date=models.DateField
    end_date=models.DateField




# Peyments Model
class Peyments(models.Model):
    id = models.IntegerField(primary_key = True)
    course_id = models.ForeignKey('Courses' ,on_delete=models.DO_NOTHING)
    user_id=models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    unique_together = [['course_id', 'user_id']]



