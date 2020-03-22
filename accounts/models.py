from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.template.defaultfilters import default
import datetime

LEXERS = [item for item in get_all_lexers() if item[1]]


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.BooleanField(default=True)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING)
    national_code = models.CharField(max_length=10)
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, default="", blank=True)
    grades = models.ManyToManyField('Grade')
    payments = models.ManyToManyField('Course', blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField('staff status', default=True)

    from accounts.managers import UserManager
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


# Roles Model
class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title



class City(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


# Grade Models
class Grade(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title



# Lesson Model
class Lesson(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    grade = models.ForeignKey('Grade', on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)
    unique_together = [['title', 'grade']]

    def __str__(self):
        return self.title


# Course Model
class Course(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    lesson = models.ForeignKey('Lesson', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def is_course_active(self):
        now = datetime.datetime.now()
        a = now - self.start_date
        b = now - self.end_date
        if a.total_seconds() >= 0 and b.total_seconds() < 0:
            return True
        else:
            return False


# Course_Calendar Model
class Course_Calendar(models.Model):
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def is_class_active(self):
        now = datetime.datetime.now()
        a = now - self.start_date
        b = now - self.end_date
        if a.total_seconds() >= 0 and b.total_seconds() < 0:
            return True
        else:
            return False



