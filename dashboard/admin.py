import jdatetime
from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from accounts.admin import InstallmentInline
from dashboard.models.course import Course
from dashboard.models.lesson import Lesson
from dashboard.models.suggestion import Suggestion
from dashboard.models import Course_Calendar, Installment
from dashboard.models import Course_Header


class InstallmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'get_start_date_decorated', 'get_end_date_decorated', 'course', 'amount']
    search_fields = ['course__title', 'title']
    inlines = (InstallmentInline,)

    def get_start_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.start_date).strftime('%y/%m/%d ')

    def get_end_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.end_date).strftime('%y/%m/%d ')

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'


# Register your models here.
admin.site.register(Course_Header)
admin.site.register(Course_Calendar)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Suggestion)
admin.site.register(Installment,InstallmentAdmin)

