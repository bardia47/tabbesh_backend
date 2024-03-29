from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.enums import AdminEnums
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .forms import *
from zarinpal.admin import PayHistoryInline
from dashboard.admin import CourseInline


class EventInline(admin.TabularInline):
    model = Event
    readonly_fields = ('change_date_decorated',)
    fields = ('related_user', 'is_active', 'type', 'change_date_decorated',)
    verbose_name_plural = "رویداد ها"
    verbose_name = "رویداد ها"
    fk_name = 'user'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EventRelatedInline(EventInline):
    fields = ('user', 'is_active', 'type', 'change_date_decorated',)
    verbose_name_plural = "رویداد های مرتبط"
    verbose_name = "رویداد های مرتبط"
    fk_name = 'related_user'


class UserAdmin(BaseUserAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js',  # jquery
            'custom_admin/js/user-admin.js'
        )

    autocomplete_fields = ('installments',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined_decorated', 'send_password_sms')
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'student_grade', 'get_full_name', 'phone_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ['last_name', 'phone_number', 'grades__title']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined_decorated')}),
        ('ارسال رمز به کاربر', {'fields': ('send_password_sms',)}),
        ('رمز عبور (در صورت ارسال نشدن رمز از این گزینه استفاده کنید)', {'fields': ('password1', 'password2',)}),
        ('اطلاعات شخص', {'fields': (
            'first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city',
            'gender',)}),
        ('دسترسی ها', {'fields': ('is_active', "role")}),
        ('اعتبار', {'fields': ('credit',)}),
        ('قسط ها ', {'fields': ('installments',)}),

    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined_decorated')}),
        ('رمز عبور', {'fields': ('password1', 'password2',)}),
        ('اطلاعات شخص', {'fields': (
            'first_name', 'last_name', 'avatar', 'grades', 'national_code', 'phone_number', 'address', 'city',
            'gender')}),
        ('دسترسی ها', {'fields': ('is_active', "role")}),
        ('اعتبار', {'fields': ('credit',)}),
    )
    inlines = [
        PayHistoryInline, EventInline, EventRelatedInline
    ]

    def get_queryset(self, request):
        return User.objects.exclude(role__code=RoleCodes.TEACHER.value).annotate(
            _student_grade=Max('grades__code')
        )

    def student_grade(self, obj):
        return obj.student_grade()

    student_grade.admin_order_field = '_student_grade'

    student_grade.short_description = 'پایه'

    def send_password_sms(self, obj):
        html = AdminEnums.forgetPasswordHtml.value
        html = html.replace('{0}', obj.phone_number)
        return mark_safe(html)

    send_password_sms.short_description = "ارسال فراموشی رمز"


class TeacherAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'phone_number', 'is_active')

    def get_fieldsets(self, request, obj=None):
        fieldsets = list((super(UserAdmin, self).get_fieldsets(request, obj)))
        fieldsets.remove((None, {'fields': ('username', 'email', 'date_joined_decorated')}), )
        try:
            fieldsets.remove(        ('قسط ها ', {'fields': ('installments',)}), )
        except:
            pass

        fieldsets.insert(0, (None, {'fields': ('username', 'email', 'date_joined_decorated', 'description')}))

        return fieldsets
    def get_inlines(self, request, obj):
        inlines = list((super(UserAdmin,self).get_inlines(request,obj)))
        inlines.append(CourseInline)
        return  inlines

    def get_queryset(self, request):
        return User.objects.filter(role__code=RoleCodes.TEACHER.value)


class CityAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


class GradeAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'is_active', 'related_user',
                    'change_date_decorated']
    list_display_links = None

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SupportAdmin(admin.ModelAdmin):
    class Meta:
        readonly_fields = ('update_date_decorated',)
        fields = (
            'title', 'code', 'update_date_decorated', 'description', 'type_choice')

    list_display = ['title', 'update_date_decorated']
    search_fields = ['title', 'code']


class MessageAdmin(admin.ModelAdmin):
    fields = ('name', 'message', 'grade',)
    list_display = ['name', 'grade', ]
    search_fields = ['name', 'grade__title', ]


# class PackageAdmin(admin.ModelAdmin):
#     search_fields = ['title', ]

class WeblogAdmin(admin.ModelAdmin):
    readonly_fields = ('update_date_decorated', 'sender', 'first_p')
    list_display = ['title', 'update_date_decorated', ]
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        obj.sender = request.user
        # obj.upload_date = datetime.datetime.now()
        super().save_model(request, obj, form, change)

    def first_p(self, obj):
        return mark_safe(obj.first_paragraph())

    first_p.short_description = 'اولین پاراگراف جهت نمایش در لیست پست ها'


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(TeacherUser, TeacherAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(Message, MessageAdmin)
# admin.site.register(Package, PackageAdmin)
admin.site.register(Slide)
admin.site.register(Weblog, WeblogAdmin)
