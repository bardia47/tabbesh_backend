from django.db import models
from jalali_date import datetime2jalali
import datetime
from tinymce import models as tinymce_models
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from core.models import AbstractBaseModel
from dashboard.enums.enum_installmentmodel import InstallmentModelEnum
from django.utils.text import slugify
# Course Model
from dashboard.apps import DashboardConfig
from django.apps import apps
from django.core.validators import MinValueValidator
from accounts.models.grade import Grade
from dashboard.models.discount import Discount
from dashboard.models.suggestion import Suggestion
from dashboard.models.lesson import Lesson
from dashboard.enums.enum_statusclass import StatusClass


class Course(AbstractBaseModel):
    lesson = models.ForeignKey(
        'Lesson', on_delete=models.DO_NOTHING, verbose_name="درس")
    grades = models.ManyToManyField(
        'accounts.Grade', blank=True, verbose_name="پایه")
    teacher = models.ForeignKey(
        'accounts.User', on_delete=models.DO_NOTHING, verbose_name="مدرس")
    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان")
    url = models.URLField("لینک", blank=True, null=True)
    slug = models.SlugField("slug", blank=True, allow_unicode=True, unique=True)
    image = models.ImageField(
        upload_to='courses_image/', default='defaults/course.jpg')
    description = tinymce_models.HTMLField(
        'توضیحات خرید درس', null=True, blank=True)
    acquaintance_video = models.URLField('ویدیو اشنایی', blank=True, null=True)
    private_description = tinymce_models.HTMLField(
        'توضیحات درس', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال',
                                    help_text='در صورتی که این گزینه غیر فعال باشد درس در قسمت خرید درس نشان داده نمیشود')
    status_classes_choices = ((StatusClass.online.value, 'انلاین'),
                              (StatusClass.offline.value, 'افلاین'))
    status = models.CharField("نوع دوره", max_length=20, choices=status_classes_choices,
                              default=StatusClass.online.value)

    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "دوره"
        verbose_name = "دوره"
        app_label = DashboardConfig.name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug_course = str(self.lesson)
        # if self.grades and self.grades.count()==1:
        #     slug_course +=  " " + self.grades.first()
        slug_course +=  " " + str(self.id)
        self.slug = slugify(slug_course, allow_unicode=True)
        super(Course, self).save()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("تاریخ پایان باید پس از تاریخ شروع باشد")

    def get_start_date_decorated(self):
        return datetime2jalali(self.start_date).strftime('%y/%m/%d _ %H:%M:%S')

    def get_end_date_decorated(self):
        return datetime2jalali(self.end_date).strftime('%y/%m/%d _ %H:%M:%S')

    def get_course_full_name(self):
        return self.lesson.__str__() + " " + self.lesson.__str__()

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'

    def get_first_class(self, exclude=None):
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
    @property
    def discount(self):
        now = datetime.datetime.now()
        query = Q(start_date__lte=now)
        query &= Q(code__isnull=True)
        query &= (Q(end_date__gte=now) | Q(end_date=None))
        query &= (Q(courses__id=self.id) | Q(courses=None))
        discount = Discount.objects.filter(query)
        if discount.exists():
            return discount.first()
        return None

    # for first future installments
    def get_next_installment(self, exclude=None):
        return self.get_next_installments().first()

    # for future installments
    def get_next_installments(self, exclude=None):
        Installment = DashboardConfig.get_model('Installment')
        now = datetime.datetime.now()
        installments = Installment.objects.filter(
            Q(start_date__gt=now) | Q(
                end_date__gt=now + datetime.timedelta(days=InstallmentModelEnum.installmentDateBefore.value)),
            course__id=self.id)
        if exclude:
            installments = installments.exclude(**exclude)
        return installments

    def students(self):
        User = apps.get_model('accounts.User')
        return User.objects.filter(installments__in=self.installment_set.all()).distinct()

    @property
    def amount(self):
        #    return self.get_next_installments().aggregate(Sum('amount'))['amount__sum']
        return self.installment_set.aggregate(Sum('amount'))['amount__sum']

    @property
    def amount_payable(self):
        discount = self.discount()
        amount = self.amount()
        if discount:
            return amount * (100 - discount.percent) / 100
        return amount

    def get_first_week_dates(self):
        calendars = self.course_calendar_set.filter(
            start_date__lt=datetime.datetime.now() + datetime.timedelta(weeks=1))
        return calendars
