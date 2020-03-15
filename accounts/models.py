from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]


# Create your models here.





class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.BooleanField(default=True)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING)
    national_code = models.CharField(max_length=10,)
    city = models.ForeignKey('City', on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField(blank=True, null=True)
    grades = models.ManyToManyField('Grade')
    payments =  models.ManyToManyField('Course')
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField('staff status',default=True)
    
    
    from accounts.managers import UserManager
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']


    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

# Roles Model
class Role(models.Model):
    id = models.IntegerField(primary_key = True)
    code = models.CharField( max_length = 10)
    title = models.CharField( max_length = 30)

# # Profile Models
# class Profile(models.Model):
#     id = models.IntegerField(primary_key= True)
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     picture_id = models.URLField()
#     gender = models.BooleanField ()
#     biography = models.TextField()
#     role_id = models.ForeignKey('Role',on_delete=models.DO_NOTHING)
#     national_code = models.CharField(max_length=10,)
#     address = models.CharField(max_length=255)

class City(models.Model):
    code = models.CharField(max_length=10,unique=True)
    title = models.CharField(max_length=30)

#Grade Models
class Grade(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)

# Relational Model Between Profiles & Grades
# class User_grade_relation(models.Model):
#     user = models.ForeignKey(User ,on_delete=models.DO_NOTHING)
#     grade = models.ForeignKey('Grade',on_delete=models.DO_NOTHING)
#     unique_together = [['user', 'grade']]


# Lesson Model
class Lesson(models.Model):
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)
    grade = models.ForeignKey('Grade' ,on_delete=models.DO_NOTHING)
    parent=models.ForeignKey('self' ,on_delete=models.DO_NOTHING)
    unique_together = [['title', 'grade']]


# Course Model
class Course(models.Model):
    code = models.CharField(max_length= 10)
    title = models.CharField(max_length= 30)
    lesson=models.ForeignKey('Lesson' ,on_delete=models.DO_NOTHING)
    teacher=models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    start_date=models.DateField
    end_date=models.DateField
    amount=models.FloatField
    url=models.URLField

# Course_Calendar Model
class Course_Calendar(models.Model):
    course=models.ForeignKey('Course' ,on_delete=models.DO_NOTHING)
    start_date=models.DateField
    end_date=models.DateField




# Payments Model
# class Payment(models.Model):
#     course = models.ForeignKey('Course' ,null=False,on_delete=models.DO_NOTHING)
#     user=models.ForeignKey(User ,null=False,on_delete=models.DO_NOTHING)
#     unique_together = [['course', 'user']]



