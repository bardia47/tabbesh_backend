import pytz
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
    username = models.CharField("نام کاربری",max_length=30, unique=True)
    password = models.CharField("رمز",max_length=128)
    email = models.EmailField('ایمیل', unique=True)
    first_name = models.CharField('نام', max_length=30, blank=True)
    last_name = models.CharField('نام خانوادگی', max_length=30, blank=True)
    date_joined = models.DateTimeField('تاریخ عضویت', auto_now_add=True)
    is_active = models.BooleanField('فعال', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.BooleanField(default=True)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING,verbose_name="نقش")
    national_code = models.CharField("کد ملی",max_length=10)
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.DO_NOTHING,verbose_name="شهر")
    address = models.CharField("آدرس",max_length=255)
    phone_number = models.CharField("تلفن همراه",max_length=12, default="", blank=True)
    grades = models.ManyToManyField('Grade', null=True, blank=True , verbose_name="پایه")
    payments = models.ManyToManyField('Course', null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField( default=True)
    
    class Meta:
        verbose_name_plural = "کاربر"

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
    code = models.CharField("کد",max_length=10)
    title = models.CharField("عنوان",max_length=30)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "نقش"


class City(models.Model):
    code = models.CharField("کد",max_length=10, unique=True)
    title = models.CharField("عنوان",max_length=30)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "شهر"


# Grade Models
class Grade(models.Model):
    code = models.CharField("کد",max_length=10)
    title = models.CharField("عنوان",max_length=30)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "پایه"



# Lesson Model
class Lesson(models.Model):
    code = models.CharField("کد",max_length=10)
    title = models.CharField("عنوان",max_length=30)
    grade = models.ForeignKey('Grade', on_delete=models.DO_NOTHING,verbose_name="پایه")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING,verbose_name="درس پدر")
    unique_together = [['title', 'grade']]

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "درس"

# Course Model
class Course(models.Model):
    code = models.CharField("کد",max_length=10)
    title = models.CharField("عنوان",max_length=30)
    lesson = models.ForeignKey('Lesson', on_delete=models.DO_NOTHING,verbose_name="درس")
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="مدرس")
    start_date = models.DateTimeField("تاریخ شروع",blank=True, null=True)
    end_date = models.DateTimeField("تاریخ پایان",blank=True, null=True)
    amount = models.FloatField("مبلغ",blank=True, null=True)
    url = models.URLField("لینک",blank=True, null=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def is_course_active(self):
        now = datetime.datetime.now(pytz.utc)
        a = now - self.start_date
        b = now - self.end_date
        if a.total_seconds() >= 0 and b.total_seconds() < 0:
            return True
        else:
            return False
        
    class Meta:
        verbose_name_plural = "دوره"    


# Course_Calendar Model
class Course_Calendar(models.Model):
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING,verbose_name="دوره")
    start_date = models.DateTimeField("تاریخ شروع",blank=True, null=True)
    end_date = models.DateTimeField("تاریخ پایان",blank=True, null=True,)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.course.title

    def is_class_active(self):
        now = datetime.datetime.now(pytz.utc)
        a = now - self.start_date
        b = now - self.end_date
        if a.total_seconds() >= 0 and b.total_seconds() < 0:
            return True
        else:
            return False
        
    class Meta:
        verbose_name_plural = "زمان برگزاری"    



