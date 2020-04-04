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

class PaymentInline(admin.StackedInline):
    model = User.payments.through
    verbose_name_plural = "پرداختی ها"
    verbose_name = "پرداختی"
    extra=0
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(PaymentInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        form.base_fields['course'].label="درس"
        widget = form.base_fields['course'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_add_related = False
        widget.can_change_related = False
        widget.label='درس'
        return formset
    
class UserCreationForm(forms.ModelForm):
    GENDERS = [(True, "پسر"), (False, "دختر")]
    password1 = forms.CharField(label='رمز', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز', widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=GENDERS, label="جنسیت" , initial='', widget=forms.Select(), required=True)

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
            'gender', 'phone_number', 'payments')
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
    list_display = ('username', 'email', 'get_full_name', 'phone_number', 'is_active')
    list_filter = ('is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined_decorated')}),
        ('در صورت نیاز رمز جدید را وارد کنید', {'fields': ('password1', 'password2',)}),
     ('اطلاعات شخص', {'fields': ('first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city', 'gender')}),
        ('دسترسی ها', {'fields': ('is_active', "role")}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2') }),
         ('اطلاعات شخص', {'fields': ('first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city', 'gender')}),

    )
    search_fields = ('username',)
    ordering = ('username',)
    inlines = [
        PaymentInline,
    ]
class CourseCalendarFormSetInline(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
           try: 
               if form.cleaned_data :
                       if not form.cleaned_data["DELETE"]: 
                           count += 1
           except AttributeError:
               pass
        if count < 1:
            raise forms.ValidationError("زمان برگذاری برای دوره تعریف نشده است") 

class CourseCalendarInline(TabularInlineJalaliMixin, admin.TabularInline):
    formset=CourseCalendarFormSetInline
    model = Course_Calendar
    max_num=3


class CourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    inlines = [
        CourseCalendarInline,
    ]
    list_display = ['code', 'title', 'get_start_jalali', 'get_end_jalali', 'teacher_full_name']
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
         context['adminform'].form.fields['teacher'].queryset  = User.objects.filter(role__code=RoleCodes.TEACHER.value)
         return super(CourseAdmin, self).render_change_form(request, context, *args, **kwargs)
     
class CourseCalendarAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['course', 'get_start_jalali', 'get_end_jalali',]
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
        if len(obj.course.course_calendar_set.all())==1 :
            self.message_user(request, "این آخرین زمان برگذاری دوره است و امکان حذف آن وجود ندارد", level=messages.ERROR)
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

# class LessonInline(admin.StackedInline):
#     model = Lesson.grades.through
#     verbose_name_plural = "پایه مرتبط"
#     verbose_name = "پایه مرتبط"
#     extra=0
#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super(LessonInline, self).get_formset(request, obj, **kwargs)
#         form = formset.form
#         form.base_fields['grade'].label="پایه"
#         widget = form.base_fields['grade'].widget
#         widget.can_add_related = False
#         widget.can_change_related = False
#         widget.can_add_related = False
#         widget.can_change_related = False
#         widget.label='پایه'
#         return formset


class LessonAdmin(admin.ModelAdmin):
        list_display = ['code', 'title']
#        exclude = ('grades',)
#         inlines = [
#         LessonInline,
#     ]
        
class GradeAdmin(admin.ModelAdmin):
        list_display = ['code', 'title']        

    
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(City, CityAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Course_Calendar, CourseCalendarAdmin)
admin.site.unregister(Group)
