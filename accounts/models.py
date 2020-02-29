from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profiles(models.Model):
    id = models.IntegerField(primary_key= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture_id = models.ForeignKey(Pictures , on_delete = models.CASCADE )
    gender = models.BooleanField ()
    biography = models.TextField()
    role_id = models.ForeignKey(Roles , on_delete = models.CASCADE)
    national_code = models.IntegerField()
    address = models.CharField(max_length=255)

# Picture Model

class Pictures(models.Model):
    id = models.IntegerField(primary_key = True)
    picture = models.ImageField()


# Roles Model
class Roles(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.IntegerField()
    title = models.CharField(max_length= 30)

# Relational Model Between Profiles & Grades
class User_grade_relation(models.Model):
    id = models.IntegerField(primary_key = True)
    user_id = models.ForeignKey(Profiles , on_delete = models.CASCADE)
    grade_id = models.ForeignKey(Grades , on_delete = models.CASCADE)
    unique_together = [['user_id', 'grade_id']]

