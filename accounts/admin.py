from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.hashers import make_password
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin    
from jalali_date import datetime2jalali, date2jalali
from django.contrib.auth.models import Group


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز', widget=forms.PasswordInput)

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
        if user.role.code == "2":
            user.is_staff = True
            user.is_superuser = True
        password = make_password(self.cleaned_data["password1"])
        user.password = password
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    GENDERS = [(True, "پسر"), (False, "دختر")]
    password1 = forms.CharField(label='رمز', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز', required=False, widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=GENDERS, label="جنسیت" , initial='', widget=forms.Select(), required=True)

    class Meta:
        model = User
        fields = (
            'username', 'role', 'email', 'city', 'grades', 'avatar', 'first_name', 'last_name', 'national_code',
            'address',
            'gender', 'phone_number', 'payments')
        labels = {
            'date_joined_decorated': "تاریخ عضویت",
        }

    def clean_password2(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if user.role.code == "2":
            user.is_staff = True
            user.is_superuser = True
        if self.data.get("password1") != '':
            password = make_password(self.cleaned_data["password1"])
            user.password = password
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):

    readonly_fields = ('date_joined_decorated',)
    
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_active')
    list_filter = ('is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined_decorated')}),
        ('در صورت نیاز رمز جدید را وارد کنید', {'fields': ('password1', 'password2',)}),
     ('اطلاعات شخص', {'fields': ('first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city', 'gender')}),
        ('دسترسی ها', {'fields': ('is_active', "role")}),
        ('پرداختی ها', {'fields': ('payments',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


class CourseCalendarInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = Course_Calendar
    extra = 0


class CourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    inlines = [
        CourseCalendarInline,
    ]
    list_display = ['code', 'title', 'get_start_jalali', 'get_end_jalali']
    search_fields = ['code', 'title']

    def get_start_jalali(self, obj):
        return datetime2jalali(obj.start_date).strftime('%y/%m/%d , %H:%M:%S')

    def get_end_jalali(self, obj):
        return datetime2jalali(obj.end_date).strftime('%y/%m/%d , %H:%M:%S')
    
    get_start_jalali.short_description = 'تاریخ شروع'
    get_start_jalali.admin_order_field = 'start_date'
    get_end_jalali.short_description = 'تاریخ پایان'
    get_end_jalali.admin_order_field = 'end_date'

    
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(City)
admin.site.register(Grade)
admin.site.register(Lesson)
admin.site.register(Course, CourseAdmin)
admin.site.unregister(Group)
