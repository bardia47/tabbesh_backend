from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from accounts.enums import RoleCodes
import datetime
import jdatetime
from tinymce import models as tinymce_models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q, Max, IntegerField
from django.db.models import Value as V
from django.db.models.functions import Concat


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
    phone_number = models.CharField("تلفن همراه", max_length=12, unique=True)
    grades = models.ManyToManyField('Grade', blank=True, verbose_name="پایه")
    # courses = models.ManyToManyField('Course', blank=True )
    installments = models.ManyToManyField('Installment', blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    credit = models.FloatField("اعتبار", default=float(0),
                               validators=[MinValueValidator(0)]
                               )

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "کاربر"
        verbose_name = "کاربر"

    from accounts.managers import UserManager
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.get_full_name()

    # get courses from user installments
    def courses(self):
        return Course.objects.filter(installment__in=self.installments.all())

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    get_full_name.short_description = 'نام'

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def date_joined_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.date_joined).strftime("%a, %d %b %Y %H:%M:%S")

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
        return self.role.code == RoleCodes.TEACHER.value

    def is_admin(self):
        return self.role.code == RoleCodes.ADMIN.value

    def is_student(self):
        return self.role.code == RoleCodes.STUDENT.value


class TeacherUser(User):
    class Meta:
        proxy = True
        verbose_name = 'اساتید'
        verbose_name_plural = 'اساتید'


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
    First = 'FIRST'
    Second = 'SECOND'
    Third = 'THIRD'
    Other = 'OTHER'
    Grade_CHOICES = ((First, 'ابتدایی'), (Second, 'متوسطه اول'), (Third, 'متوسطه دوم'),
                     (Other, 'مهارتی'))
    grade_choice = models.CharField("پایه", max_length=10, choices=Grade_CHOICES, default='Other')
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
    grades = models.ManyToManyField('Grade', blank=True, verbose_name="پایه")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="درس پدر")
    unique_together = [['title', 'grade']]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "درس"
        verbose_name = "درس"


# Course Model
class Course(models.Model):
    code = models.CharField("کد", max_length=10, unique=True)
    title = models.CharField("عنوان", max_length=30)
    lesson = models.ForeignKey('Lesson', on_delete=models.DO_NOTHING, verbose_name="درس")
    grade = models.ForeignKey('Grade', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="پایه")
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="مدرس")
    start_date = models.DateTimeField("تاریخ شروع")
    end_date = models.DateTimeField("تاریخ پایان")
    # amount = models.FloatField("مبلغ", default=float(0),
    #                             validators=[MinValueValidator(0)]
    #                             )
    url = models.URLField("لینک", blank=True, null=True)
    image = models.ImageField(upload_to='courses_image/', default='defaults/course.jpg')
    description = tinymce_models.HTMLField('توضیحات خرید درس', null=True, blank=True)
    private_description = tinymce_models.HTMLField('توضیحات درس', null=True, blank=True)

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
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")

    def get_first_class(self, exclude=None):
        if len(self.course_calendar_set.all()) == 0:
            return None
        return self.course_calendar_set.first()

    def get_next_class(self, exclude=None):
        if len(self.course_calendar_set.all()) == 0:
            return None
        now = datetime.datetime.now()
        return self.course_calendar_set.filter(end_date__gte=now).first()

    def get_parent_lesson(self, exclude=None):
        lesson = self.lesson
        while True:
            if lesson.parent is None:
                return lesson
            else:
                lesson = lesson.parent

    # get discount without code
    def get_discount(self, exclude=None):
        now = datetime.datetime.now()
        query = Q(start_date__lte=now)
        query &= Q(code__isnull=True)
        query &= (Q(end_date__gte=now) | Q(end_date=None))
        query &= (Q(courses__id=self.id) | Q(courses=None))
        discount = Discount.objects.filter(query)
        if discount.exists():
            return discount.first()
        return None

    def get_next_installment(self, exclude=None):
        now = datetime.datetime.now()
        installment = Installment.objects.filter(
            Q(start_date__gt=now) | Q(end_date__gt=now + datetime.timedelta(days=10))).first()
        return installment

    def students(self):
        return User.objects.filter(installments__in=self.installment_set.all())


# Course_Calendar Model
class Course_Calendar(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="دوره")
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
        a = now - self.start_date + datetime.timedelta(minutes=5)
        b = now - self.end_date
        if a.total_seconds() >= 0 and b.total_seconds() < 0:
            return True
        else:
            return False

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.start_date or not self.end_date or self.end_date < self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")


def document_directory_path(instance, filename):
    return 'documents/{0}/{1}'.format(instance.course.code, filename)


# Documents_model
class Document(models.Model):
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING, verbose_name="دوره")
    upload_document = models.FileField('فایل', upload_to=document_directory_path, null=True, blank=True)
    upload_date = models.DateTimeField("تاریخ بارگذاری", auto_now_add=True)
    title = models.CharField("عنوان", max_length=60)
    description = models.TextField("توضیحات", null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="فرد بارگذار")

    class Meta:
        ordering = ['-upload_date']
        verbose_name_plural = "فایل ها"
        verbose_name = "فایل ها"

    def __str__(self):
        return self.title

    def upload_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.upload_date).strftime("%a, %d %b %Y %H:%M:%S")

    upload_date_decorated.short_description = 'تاریخ بارگذاری'


class Pay_History(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="خریدار")
    amount = models.FloatField("هزینه", default=float(0))
    is_successful = models.BooleanField('موفق', default=False)
    submit_date = models.DateTimeField("تاریخ ثبت", null=True)
    installments = models.TextField()
    payment_code = models.CharField("شناسه پرداخت", max_length=20)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "سوابق خرید"
        verbose_name = "سوابق خرید"

    def submit_date_decorated(self):
        if self.submit_date:
            return jdatetime.datetime.fromgregorian(datetime=self.submit_date).strftime("%a, %d %b %Y %H:%M:%S")
        else:
            "-"

    def get_installments(self):
        installments_id_list = self.installments.split()
        return list(Installment.objects.filter(id__in=installments_id_list).annotate(
            full_title=Concat('title', V(' '), 'course__title')).values_list('full_title', flat=True))

    get_installments.short_description = 'قسط های خریداری شده'
    submit_date_decorated.short_description = 'تاریخ ثبت'


class Discount(models.Model):
    title = models.CharField("نام تخفیف", max_length=30, null=True, blank=True, unique=True)
    code = models.CharField("کد", max_length=15, null=True, blank=True, unique=True)
    percent = models.IntegerField("درصد",
                                  default=10,
                                  validators=[
                                      MaxValueValidator(100),
                                      MinValueValidator(1)
                                  ]
                                  )
    start_date = models.DateTimeField("تاریخ شروع")
    end_date = models.DateTimeField("تاریخ پایان", null=True, blank=True)
    courses = models.ManyToManyField('Course', blank=True, verbose_name="درس های تخفیف خورده")

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "تخفیف"
        verbose_name = "تخفیف"

    def __str__(self):
        return str(self.title)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد یا خالی باشد")


class DiscountWithoutCode(Discount):
    class Meta:
        proxy = True
        verbose_name = 'تخفیف بدون کد'
        verbose_name_plural = 'تخفیف بدون کد'


class Event(models.Model):
    # Introducer = 'INER'
    # just create model with INING
    Introducing = 'INING'
    TYPE_CHOICES = [
        # (Introducer, 'معرفی کننده'),
        (Introducing, 'معرفی شونده'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر", related_name='event')
    change_date = models.DateTimeField("تاریخ آخرین تغییر", auto_now=True)
    type = models.CharField('نوع', max_length=5, choices=TYPE_CHOICES)
    is_active = models.BooleanField('فعال', default=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر مرتبط",
                                     related_name='event_related', blank=True, null=True)

    class Meta:
        ordering = ['is_active', '-change_date']
        verbose_name_plural = "رویداد"
        verbose_name = "رویداد"

    def change_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.change_date).strftime("%a, %d %b %Y %H:%M:%S")

    change_date_decorated.short_description = 'تاریخ آخرین تغییر'


# Course Model
class Support(models.Model):
    public = 'PUBLIC'
    teacher = 'TEACHER'
    TYPE_CHOICES = ((public, 'عمومی'), (teacher, 'استاد'),)
    type_choice = models.CharField("نوع", max_length=7, choices=TYPE_CHOICES, default='PUBLIC')
    code = models.CharField("کد", max_length=10, unique=True)
    title = models.CharField("عنوان", max_length=30)
    description = models.TextField('توضیحات', null=True, blank=True)
    update_date = models.DateTimeField("تاریخ آخرین تغییر", auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = "پشتیبانی"
        verbose_name = "پشتیبانی"

    def __str__(self):
        return self.title

    def update_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.update_date).strftime("%a, %d %b %Y %H:%M:%S")

    update_date_decorated.short_description = 'تاریخ آخرین تغییر'


# comment it because it can be heavy on server

# this signal clear the cache after adding a new course or support we can add it for other table like user
# because of counter but i think this happens a lot and make caching useless
# @receiver(post_save, sender=Course)
# @receiver(post_save, sender=Support)
# def clear_cache(sender, instance, **kwargs):
#     cache.clear()


# Installment model Model
class Installment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="دوره")
    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان")
    title = models.CharField("عنوان", max_length=30)
    amount = models.FloatField("مبلغ", default=float(0),
                               validators=[MinValueValidator(0)]
                               )

    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "قسط"
        verbose_name = "قسط"

    def __str__(self):
        return self.title + " " + self.course.title

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.start_date or not self.end_date or self.end_date < self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")
        query = Q(course__id=self.course.id)
        if self.id is not None:
            query &= ~Q(id=self.id)
        query &= ((Q(start_date__gte=self.start_date) & (Q(end_date__lte=self.end_date))) |
                  (Q(start_date__lte=self.start_date) & (Q(end_date__gte=self.end_date))) |
                  (Q(start_date__lte=self.start_date) & (Q(end_date__lte=self.end_date)) & (
                      Q(end_date__gte=self.start_date))) |
                  (Q(start_date__gte=self.start_date) & (Q(start_date__lte=self.end_date)) & (
                      Q(end_date__gte=self.end_date)))
                  )
        if Installment.objects.filter(query).exists():
            raise ValidationError("تاریخ قسط تداخل دارد")

    def get_amount_payable(self, exclude=None):
        discount = self.course.get_discount()
        if discount:
            return self.amount * (100 - discount.percent) / 100
        return self.amount

    def get_discount_amount(self, exclude=None):
        discount = self.course.get_discount()
        if discount:
            return self.amount * discount.percent / 100
        return 0
