from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from jalali_date import datetime2jalali
from accounts.apps import AccountsConfig
from accounts.enums.enum_role_code import RoleCodeEnum
import datetime
from tinymce import models as tinymce_models
from django.core.validators import MinValueValidator
from core.validators import PERSIAN_REGEX_VALIDATOR, PHONE_NUMBER_REGEX_VALIDATOR
# Create your models here.
from dashboard.enums.enum_installmentmodel import InstallmentModelEnum
from dashboard.enums.enum_statusclass import StatusClass
from dashboard.models import Course
from django.db.models import Q


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField("تلفن همراه", max_length=12, unique=True, validators=[PHONE_NUMBER_REGEX_VALIDATOR])
    password = models.CharField("رمز", max_length=128)
    # email = models.EmailField('ایمیل', unique=True, null=True, blank=True)
    first_name = models.CharField('نام', max_length=30, validators=[PERSIAN_REGEX_VALIDATOR])
    last_name = models.CharField('نام خانوادگی', max_length=30, validators=[PERSIAN_REGEX_VALIDATOR])
    description = tinymce_models.HTMLField('توضیحات معلم', null=True, blank=True)
    date_joined = models.DateTimeField('تاریخ عضویت', auto_now_add=True)
    is_active = models.BooleanField('فعال', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.BooleanField(default=True)
    role = models.ForeignKey(
        'Role', on_delete=models.DO_NOTHING, verbose_name="نقش")
    # national_code = models.CharField(
    #     "کد ملی", max_length=10, null=True, blank=True)
    city = models.ForeignKey(
        'City', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="شهر")
    address = models.CharField("آدرس", max_length=255, null=True, blank=True)
    grades = models.ManyToManyField('Grade', blank=True, verbose_name="پایه")
    # courses = models.ManyToManyField('Course', blank=True )
    is_superuser = None
    credit = models.FloatField("اعتبار", default=float(0),
                               validators=[MinValueValidator(0)]
                               )

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "کاربر"
        verbose_name = "کاربر"
        app_label = AccountsConfig.name

    from accounts.managers import UserManager
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    # get courses from user installments
    def courses(self):
        return Course.objects.filter(installment__in=self.installment_set.all()).distinct()

    def offline_courses(self):
        return Course.objects.filter(installment__in=self.installment_set.all(),status=StatusClass.offline.value).distinct()

    def online_courses(self):
        return Course.objects.filter(installment__in=self.installment_set.all(),status=StatusClass.online.value).distinct()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    get_full_name.short_description = 'نام'

    def date_joined_decorated(self):
        return datetime2jalali(self.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    date_joined_decorated.short_description = 'تاریخ عضویت'

    def set_default_avatar(self):
        if not self.avatar:
            if self.is_teacher():
                self.avatar = "defaults/teacher.png"
            else:
                self.avatar = "defaults/student.png"

    def __str__(self):
        return self.get_full_name()

    def student_grade(self):
        try:
            return self.grades.all().first().title
        except:
            return ""

    def is_teacher(self):
        return self.role.code == RoleCodeEnum.TEACHER.value

    def is_admin(self):
        return self.role.code == RoleCodeEnum.ADMIN.value

    def is_student(self):
        return self.role.code == RoleCodeEnum.STUDENT.value

    @property
    def is_staff(self):
        return self.is_admin()

    @property
    def is_superuser(self):
        return self.is_admin()


class TeacherUser(User):
    class Meta:
        proxy = True
        verbose_name = 'اساتید'
        verbose_name_plural = 'اساتید'
        app_label = AccountsConfig.name

    # get courses of teacher showing in shopping
    def get_shopping_courses(self):
        now = datetime.datetime.now()
        return Course.objects.filter(teacher=self.id, is_active=True, end_date__gt=now + datetime.timedelta(
            days=InstallmentModelEnum.installmentDateBefore.value))

# Roles Model
