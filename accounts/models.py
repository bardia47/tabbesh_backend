import pytz
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.template.defaultfilters import default
from accounts.enums import RoleCodes
import datetime
import jdatetime
from django.core.exceptions import ValidationError

# import for compress images
import sys 
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

LEXERS = [item for item in get_all_lexers() if item[1]]

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("نام کاربری", max_length=30, unique=True)
    password = models.CharField("رمز", max_length=128)
    email = models.EmailField('ایمیل', unique=True, null=True, blank=True)
    first_name = models.CharField('نام', max_length=30, blank=True)
    last_name = models.CharField('نام خانوادگی', max_length=30, blank=True)
    date_joined = models.DateTimeField('تاریخ عضویت', auto_now_add=True)
    is_active = models.BooleanField('فعال', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.BooleanField(default=True)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, verbose_name="نقش")
    national_code = models.CharField("کد ملی", max_length=10, null=True, blank=True)
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="شهر")
    address = models.CharField("آدرس", max_length=255, null=True, blank=True)
    phone_number = models.CharField("تلفن همراه", max_length=12, default="", blank=True)
    grades = models.ManyToManyField('Grade', blank=True, verbose_name="پایه")
    payments = models.ManyToManyField('Course', blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    #compress images
    def compressImage(self,uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((20,20), Image.ANTIALIAS) 
        imageTemproary = imageTemproary.convert('RGB')
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage
    class Meta:
        verbose_name_plural = "کاربر"
        verbose_name = "کاربر"

    from accounts.managers import UserManager
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    get_full_name.short_description = 'نام'

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def date_joined_decorated(self):
        print(self.date_joined)
        return jdatetime.datetime.fromgregorian(datetime=self.date_joined).strftime("%a, %d %b %Y %H:%M:%S")
    
    def set_default_avatar(self):
        if not self.avatar :
            if self.role.code == RoleCodes.TEACHER.value:     
                self.avatar = "defaults/teacher.png"
            else :
                self.avatar = "defaults/student.png"
    
        print(self.avatar)        


# Roles Model
class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField("کد", max_length=10)
    title = models.CharField("عنوان", max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "نقش"
        verbose_name = "نقش"


class City(models.Model):
    code = models.CharField("کد", max_length=10, unique=True)
    title = models.CharField("عنوان", max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "شهر"
        verbose_name = "شهر"


# Grade Models
class Grade(models.Model):
    code = models.CharField("کد", max_length=10)
    title = models.CharField("عنوان", max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['code']
        verbose_name_plural = "پایه"
        verbose_name = "پایه"


# Lesson Model
class Lesson(models.Model):
    code = models.CharField("کد", max_length=10)
    title = models.CharField("عنوان", max_length=30)
    grade = models.ForeignKey('Grade', on_delete=models.DO_NOTHING, verbose_name="پایه")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="درس پدر")
    unique_together = [['title', 'grade']]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "درس"
        verbose_name = "درس"


# Course Model
class Course(models.Model):
    code = models.CharField("کد", max_length=10)
    title = models.CharField("عنوان", max_length=30)
    lesson = models.ForeignKey('Lesson', on_delete=models.DO_NOTHING, verbose_name="درس")
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="مدرس")
    start_date = models.DateTimeField("تاریخ شروع")
    end_date = models.DateTimeField("تاریخ پایان")
    amount = models.FloatField("مبلغ", default=float(0))
    url = models.URLField("لینک", blank=True, null=True)
    image = models.ImageField(upload_to='courses_image/', default='defaults/course.jpg')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "دوره"
        verbose_name = "دوره"

    def __str__(self):
        return self.title

    # def is_course_active(self):
    #     now = datetime.datetime.now()
    #     a = now - self.start_date
    #     b = now - self.end_date
    #     if a.total_seconds() >= 0 and b.total_seconds() < 0:
    #         return True
    #     else:
    #         return False
        
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.end_date < self.start_date :
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")
        if self.teacher.role.code != RoleCodes.TEACHER.value:
            raise ValidationError("مدرس باید نقش مدرس داشته باشد")


# Course_Calendar Model
class Course_Calendar(models.Model):
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING, verbose_name="دوره")
    start_date = models.DateTimeField("تاریخ شروع")
    end_date = models.DateTimeField("تاریخ پایان")

    class Meta:
        ordering = ['end_date']
        verbose_name_plural = "زمان برگزاری"
        verbose_name = "زمان برگزاری"

    def __str__(self):
        return self.course.title

    def is_class_active(self):
        now = datetime.datetime.now()
        a = now - self.start_date
        b = now - self.end_date
        if a.total_seconds() >= 0 and b.total_seconds() < 0:
            return True
        else:
            return False
        
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.start_date or not self.end_date or self.end_date < self.start_date :
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")
        
