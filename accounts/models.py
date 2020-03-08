from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Roles Model
class Role(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)

# Profile Models
class Profile(models.Model):
    id = models.IntegerField(primary_key= True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture_id = models.URLField()
    gender = models.BooleanField ()
    biography = models.TextField()
    role_id = models.ForeignKey('Role',on_delete=models.DO_NOTHING)
    national_code = models.CharField(max_length=10,)
    address = models.CharField(max_length=255)


#Grade Models
class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)

# Relational Model Between Profiles & Grades
class User_grade_relation(models.Model):
    id = models.IntegerField(primary_key = True)
    user_id = models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    grade_id = models.ForeignKey('Grade',on_delete=models.DO_NOTHING)
    unique_together = [['user_id', 'grade_id']]


# Lesson Model
class Lesson(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)
    grade_id = models.ForeignKey('Grade' ,on_delete=models.DO_NOTHING)
    lesson_id=models.ForeignKey('Lesson' ,on_delete=models.DO_NOTHING)
    unique_together = [['title', 'grade_id']]


# Course Model
class Course(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)
    lesson_id=models.ForeignKey('Lesson' ,on_delete=models.DO_NOTHING)
    teacher_id=models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    start_date=models.DateField
    end_date=models.DateField
    amount=models.FloatField
    url=models.URLField

# Course_Calendar Model
class Course_Calendar(models.Model):
    id = models.IntegerField(primary_key = True)
    course_id=models.ForeignKey('Course' ,on_delete=models.DO_NOTHING)
    start_date=models.DateField
    end_date=models.DateField




# Peyments Model
class Peyment(models.Model):
    id = models.IntegerField(primary_key = True)
    course_id = models.ForeignKey('Course' ,on_delete=models.DO_NOTHING)
    user_id=models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    unique_together = [['course_id', 'user_id']]



