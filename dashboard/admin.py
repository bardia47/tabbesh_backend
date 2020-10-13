from django.contrib import admin
from accounts.models import *
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin
from accounts.enums import RoleCodes
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from zarinpal.admin import DiscountWithoutCodeInline, InstallmenCoursetInline
from .forms import *
from .validators import AdminValidator


class CourseCalendarInline(TabularInlineJalaliMixin, admin.TabularInline):
    # formset = CourseCalendarFormSetInline
    model = Course_Calendar
    max_num = 3


class LessonAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


class CourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    form = CourseForm
    inlines = [
        CourseCalendarInline,
        DiscountWithoutCodeInline,
        InstallmenCoursetInline
    ]
    list_display = ['code', 'title', 'get_start_date_decorated', 'get_end_date_decorated', 'teacher', 'student_link']
    search_fields = ['code', 'title']

    def get_start_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.start_date).strftime('%y/%m/%d')

    def get_end_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.end_date).strftime('%y/%m/%d')

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['teacher'].queryset = User.objects.filter(role__code=RoleCodes.TEACHER.value)
        AdminValidator.showErrorsOfCourse(kwargs['obj'], request)
        return super(CourseAdmin, self).render_change_form(request, context, *args, **kwargs)

    def save_related(self, request, form, formsets, change):
        super(CourseAdmin, self).save_related(request, form, formsets, change)
        AdminValidator.showErrorsOfCourse(form.instance, request)

    def student_link(self, obj):
        return mark_safe('<a href="{0}">{1}</a>'.format(
            reverse("teacher_course_panel", args=(obj.code,)),
            "پنل اساتید"
        ))

    student_link.short_description = "پنل اساتید"


class CourseCalendarAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['course', 'get_start_date_decorated', 'get_end_date_decorated', ]
    search_fields = ['course']

    def get_start_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.start_date).strftime('%y/%m/%d , %H:%M:%S')

    def get_end_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.end_date).strftime('%y/%m/%d , %H:%M:%S')

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'

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
        # obj.upload_date = datetime.datetime.now()
        super().save_model(request, obj, form, change)


admin.site.register(Course, CourseAdmin)
admin.site.register(Course_Calendar, CourseCalendarAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Document, DocumentAdmin)
