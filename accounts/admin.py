from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.hashers import make_password
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from jalali_date import datetime2jalali, date2jalali
from django.contrib.auth.models import Group
from accounts.enums import RoleCodes
from django.contrib import messages
from django.contrib.admin.options import InlineModelAdmin
import datetime
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms
from django.forms.models import BaseInlineFormSet

class CourseInline(admin.StackedInline):
    model = User.courses.through
    verbose_name_plural = "دوره ها"
    verbose_name = "دوره ها"
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CourseInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        form.base_fields['course'].label = "دوره"
        widget = form.base_fields['course'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_add_related = False
        widget.can_change_related = False
        widget.label = 'دوره'
        return formset


class PayHistoryInline(admin.TabularInline):
    model = Pay_History
    readonly_fields = ('submit_date_decorated',)
    fields = ('amount', 'is_successful', 'submit_date_decorated', 'payment_code')
    verbose_name_plural = "پرداختی ها"
    verbose_name = "پرداختی"

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserCreationForm(forms.ModelForm):
    GENDERS = [(True, "پسر"), (False, "دختر")]
    password1 = forms.CharField(label='رمز', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز', widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=GENDERS, label="جنسیت", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if user.role.code == RoleCodes.ADMIN.value:
            user.is_superuser = True
        else:
            user.is_superuser = False

        if self.data.get("password1") != '':
            password = make_password(self.cleaned_data["password1"])
            user.password = password
        user.set_default_avatar()
        if commit:
            user.save()
        return user

        if commit:
            user.save()
        return user


class UserChangeForm(UserCreationForm):
    password1 = forms.CharField(label='رمز', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز', required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username', 'role', 'email', 'city', 'grades', 'avatar', 'first_name', 'last_name', 'national_code',
            'address',
            'gender', 'phone_number', 'courses')
        labels = {
            'date_joined_decorated': "تاریخ عضویت",
        }

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if user.role.code == RoleCodes.ADMIN.value:
            user.is_superuser = True
        else:
            user.is_superuser = False

        if self.data.get("password1") != '':
            password = make_password(self.cleaned_data["password1"])
            user.password = password
        user.set_default_avatar()
        if commit:
            user.save()
        return user

        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    readonly_fields = ('date_joined_decorated',)

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'get_student_grade', 'get_full_name', 'phone_number', 'is_active')
    list_filter = ('is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined_decorated')}),
        ('در صورت نیاز رمز جدید را وارد کنید', {'fields': ('password1', 'password2',)}),
        ('اطلاعات شخص', {'fields': (
        'first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city', 'gender')}),
        ('دسترسی ها', {'fields': ('is_active', "role")}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2')}),
        ('اطلاعات شخص', {'fields': (
        'first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city', 'gender')}),

    )
    search_fields = ['last_name','phone_number']
    ordering = ('username',)
    inlines = [
        CourseInline, PayHistoryInline
    ]

    def get_queryset(self, request):
        return  User.objects.exclude(role__code=RoleCodes.TEACHER.value)


class TeacherUser(User):
    class Meta:
        proxy = True
        verbose_name = 'اساتید'
        verbose_name_plural = 'اساتید'

class TeacherAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'phone_number', 'is_active')
    def get_queryset(self, request):
        return User.objects.filter(role__code=RoleCodes.TEACHER.value)


class CourseCalendarFormSetInline(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    if not form.cleaned_data["DELETE"]:
                        count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError("زمان برگذاری برای دوره تعریف نشده است")


class CourseCalendarInline(TabularInlineJalaliMixin, admin.TabularInline):
    formset = CourseCalendarFormSetInline
    model = Course_Calendar
    max_num = 3

class DiscountWithoutCodeInline(admin.TabularInline):
    model = Course.discount_set.through
    max_num = 1

    verbose_name_plural = "تخفیف بدون کد"
    verbose_name =  "تخفیف بدون کد"

    def get_queryset(self, request):
        qs = super(DiscountWithoutCodeInline, self).get_queryset(request)
        return qs.filter(discount__code__isnull=True)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(DiscountWithoutCodeInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        if db_field.name == 'discount':
            field.limit_choices_to = {'code__isnull': "True"}
        return field


class CourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [
        CourseCalendarInline,
        DiscountWithoutCodeInline
    ]
    list_display = ['code', 'title', 'get_start_jalali', 'get_end_jalali', 'teacher_full_name','student_link']
    search_fields = ['code', 'title']

    def teacher_full_name(self, obj):
        return obj.teacher.get_full_name()

    teacher_full_name.short_description = 'نام مدرس'
    teacher_full_name.admin_order_field = 'teacher__get_full_name'

    def get_start_jalali(self, obj):
        return datetime2jalali(obj.start_date).strftime('%y/%m/%d , %H:%M:%S')

    def get_end_jalali(self, obj):
        return datetime2jalali(obj.end_date).strftime('%y/%m/%d , %H:%M:%S')

    get_start_jalali.short_description = 'تاریخ شروع'
    get_start_jalali.admin_order_field = 'start_date'
    get_end_jalali.short_description = 'تاریخ پایان'
    get_end_jalali.admin_order_field = 'end_date'

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['teacher'].queryset = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        return super(CourseAdmin, self).render_change_form(request, context, *args, **kwargs)

    def student_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("student_list", args=(obj.code,)),
            "لیست دانش آموزان"
        ))
    student_link.short_description = ' لیست دانش آموزان'


class CourseCalendarAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['course', 'get_start_jalali', 'get_end_jalali', ]
    search_fields = ['course']

    def get_start_jalali(self, obj):
        return datetime2jalali(obj.start_date).strftime('%y/%m/%d , %H:%M:%S')

    def get_end_jalali(self, obj):
        return datetime2jalali(obj.end_date).strftime('%y/%m/%d , %H:%M:%S')

    get_start_jalali.short_description = 'تاریخ شروع'
    get_start_jalali.admin_order_field = 'start_date'
    get_end_jalali.short_description = 'تاریخ پایان'
    get_end_jalali.admin_order_field = 'end_date'

    def delete_model(self, request, obj):
        if len(obj.course.course_calendar_set.all()) == 1:
            self.message_user(request, "این آخرین زمان برگذاری دوره است و امکان حذف آن وجود ندارد",
                              level=messages.ERROR)
            return self
        admin.ModelAdmin.delete_model(self, request, obj)

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_delete(self, request, obj_display, obj_id):
        response = super().response_delete(request, obj_display, obj_id)
        self.remove_default_message(request)
        return response


class CityAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


class GradeAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


class DocumentAdmin(admin.ModelAdmin):
    class Meta:
        labels = {
            'upload_date_decorated': 'تاریخ بارگذاری',
        }

    readonly_fields = ('upload_date_decorated', 'sender')
    fields = (
        'title', 'upload_date_decorated', 'sender', 'course', 'upload_document', 'description')
    list_display = ['title', 'course', 'upload_date_decorated']
    search_fields = ['title', 'course']

    def save_model(self, request, obj, form, change):
        obj.sender = request.user
        obj.upload_date = datetime.datetime.now()
        super().save_model(request, obj, form, change)


class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ['purchaser_link', 'amount', 'is_successful', 'get_submit_date_decorated', 'payment_code', 'get_courses']
    fields = (
        'purchaser', 'amount', 'is_successful', 'get_submit_date_decorated', 'payment_code', 'get_courses')
    exclude = ['courses', ]
    readonly_fields = ('purchaser_link',)

    def get_submit_date_decorated(self, obj):
        if obj.submit_date:
            return datetime2jalali(obj.submit_date).strftime('%y/%m/%d , %H:%M:%S')
        else:
            "-"

    get_submit_date_decorated.short_description = 'تاریخ ثبت'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def purchaser_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:accounts_user_change", args=(obj.purchaser.pk,)),
            obj.purchaser
        ))



class CourseDiscountFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
               if not form.errors and form.is_valid and  form.cleaned_data and not form.cleaned_data.get('DELETE') :
                    discount_id=form.cleaned_data['discount'].id
                    discount = Discount.objects.filter(courses__id=form.cleaned_data['course'].id,code__isnull=True ).exclude(id=discount_id)
                    count = count + 1
                    if discount:
                        raise forms.ValidationError("درس " + form.cleaned_data['course'].title + " دارای تخفیف میباشند")
        if count>0:
            discount = Discount.objects.filter(courses=None , code__isnull=True).exclude(id=discount_id)
            if discount:
                raise forms.ValidationError("تمامی دروس دارای تخفیف میباشند")

class CourseDiscountInline(TabularInlineJalaliMixin,admin.TabularInline):
    formset = CourseDiscountFormSet
    model = Discount.courses.through
    verbose_name_plural = "دروس مشمول تخفیف(در صورت خالی بودن تمام دروس شامل تخفیف میشوند)"
    verbose_name = "دروس مشمول تخفیف"

    def get_formset(self, request, obj=None, **kwargs):
            formset = super(CourseDiscountInline, self).get_formset(request, obj, **kwargs)
            form = formset.form
            form.base_fields['course'].label = "دوره"
            widget = form.base_fields['course'].widget
            widget.label = 'دوره'
            return formset



class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('title', 'code', 'percent', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
            super(DiscountForm, self).__init__(*args, **kwargs)
            self.fields['code'].required = True

class DiscountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['code', 'title','percent', 'get_start_jalali', 'get_end_jalali']
    search_fields = ['code', 'title']
    form = DiscountForm
    inlines = [
        CourseDiscountInline
    ]

    def get_queryset(self, request):
        return Discount.objects.filter(code__isnull=False)

    def get_start_jalali(self, obj):
        return datetime2jalali(obj.start_date).strftime('%y/%m/%d ')

    def get_end_jalali(self, obj):
        if obj.end_date:
            return datetime2jalali(obj.end_date).strftime('%y/%m/%d')
        return ""

    get_start_jalali.short_description = 'تاریخ شروع'
    get_start_jalali.admin_order_field = 'start_date'
    get_end_jalali.short_description = 'تاریخ پایان'
    get_end_jalali.admin_order_field = 'end_date'

class DiscountWithoutCode(Discount):
    class Meta:
        proxy = True
        verbose_name = 'تخفیف بدون کد'
        verbose_name_plural = 'تخفیف بدون کد'

class DiscountWithoutCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountWithoutCode
        fields = ('title', 'percent', 'start_date', 'end_date')

class DiscountWithoutCodeAdmin(DiscountAdmin):
    form= DiscountWithoutCodeForm

    def get_queryset(self, request):
        return Discount.objects.filter(code__isnull=True)

admin.site.register(User, UserAdmin)
admin.site.register(TeacherUser, TeacherAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Course_Calendar, CourseCalendarAdmin)
admin.site.unregister(Group)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Pay_History, PayHistoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountWithoutCode, DiscountWithoutCodeAdmin)

