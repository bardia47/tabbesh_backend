from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , primary_key = True)
    state = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    mobile_phone = models.CharField(max_length=30)
    home_phone = models.CharField(max_length=30 , blank= True)
    profile_image = models.ImageField()

    