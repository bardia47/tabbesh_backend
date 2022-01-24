# from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.utils.text import slugify
# from jalali_date import datetime2jalali
# from accounts.enums.enum_role_code import RoleCodeEnum
# import datetime
# from tinymce import models as tinymce_models
# from django.core.exceptions import ValidationError
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db.models import Q, Sum
#
# from core.models import AbstractBaseModel
#
# class Event(models.Model):
#     # Introducer = 'INER'
#     # just create model with INING
#     Introducing = 'INING'
#     TYPE_CHOICES = [
#         # (Introducer, 'معرفی کننده'),
#         (Introducing, 'معرفی شونده'),
#     ]
#     user = models.ForeignKey(
#         'User', on_delete=models.CASCADE, verbose_name="کاربر", related_name='event')
#     change_date = models.DateTimeField("تاریخ آخرین تغییر", auto_now=True)
#     type = models.CharField('نوع', max_length=5, choices=TYPE_CHOICES)
#     is_active = models.BooleanField('فعال', default=True)
#     related_user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="کاربر مرتبط",
#                                      related_name='event_related', blank=True, null=True)
#
#     class Meta:
#         ordering = ['is_active', '-change_date']
#         verbose_name_plural = "رویداد"
#         verbose_name = "رویداد"
#
#     def change_date_decorated(self):
#         return datetime2jalali(self.change_date).strftime('%y/%m/%d _ %H:%M:%S')
#
#     change_date_decorated.short_description = 'تاریخ آخرین تغییر'
#
#
# # Course Model
# class Support(AbstractBaseModel):
#     public = 'PUBLIC'
#     teacher = 'TEACHER'
#     TYPE_CHOICES = ((public, 'عمومی'), (teacher, 'استاد'),)
#     type_choice = models.CharField(
#         "نوع", max_length=7, choices=TYPE_CHOICES, default='PUBLIC')
#     description = models.TextField('توضیحات', null=True, blank=True)
#     update_date = models.DateTimeField("تاریخ آخرین تغییر", auto_now=True)
#
#     class Meta:
#         ordering = ['title']
#         verbose_name_plural = "پشتیبانی"
#         verbose_name = "پشتیبانی"
#
#     def __str__(self):
#         return self.title
#
#     def update_date_decorated(self):
#         return datetime2jalali(self.update_date).strftime('%y/%m/%d _ %H:%M:%S')
#
#     update_date_decorated.short_description = 'تاریخ آخرین تغییر'
#
# class Message(models.Model):
#     name = models.CharField('اسم', max_length=50)
#     message = tinymce_models.HTMLField('پیام')
#     grade = models.ForeignKey('Grade', verbose_name='پایه', on_delete=models.SET_NULL, null=True, blank=True)
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name_plural = 'پیام ها'
#         verbose_name = 'پیام'
#
#     def __str__(self):
#         return self.name
#
#
# class Slide(models.Model):
#     url = models.URLField('لینک')
#     image = models.ImageField('عکس', upload_to='slides/')
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name_plural = 'اسلاید ها'
#         verbose_name = 'اسلاید'
#
#     def __str__(self):
#         return self.url
#
# class Weblog(models.Model):
#     title = models.CharField("عنوان", max_length=40)
#     image = models.ImageField('عکس', upload_to='weblog/')
#     text = tinymce_models.HTMLField('متن')
#     pub_date = models.DateTimeField("تاریخ", auto_now_add=True)
#     slug = models.SlugField('لینک', allow_unicode=True, unique=True, blank=True,
#                             help_text='نحوه نمایش آدرس پست در صورت خالی ماندن از عنوان پست برای ساخت لینک استفاده می شود.')
#     sender = models.ForeignKey(
#         'User', on_delete=models.DO_NOTHING, verbose_name="فرد بارگذار")
#
#     class Meta:
#         ordering = ['-pub_date']
#         verbose_name_plural = 'پست ها'
#         verbose_name = 'پست'
#
#     def __str__(self):
#         return self.title
#
#     def clean(self):
#         if self.slug == '':
#             self.slug = slugify(self.title, allow_unicode=True)
#
#     def update_date_decorated(self):
#         return datetime2jalali(self.pub_date).strftime('%y/%m/%d _ %H:%M:%S')
#
#     update_date_decorated.short_description = 'تاریخ انتشار پست'
#
#     def first_paragraph(self):
#         return self.text.split('\r\n')[0]
