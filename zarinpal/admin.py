from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import *
from accounts.models import *

class InstallmentUserInline(admin.StackedInline):
    formset =  InstallmentUserInlineForm
    model = User.installments.through
    verbose_name_plural = "قسط ها"
    verbose_name = "قسط ها"
    extra = 0


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

class InstallmenCoursetInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = Installment
    max_num = 3

class DiscountWithoutCodeInline(admin.TabularInline):
    model = Course.discount_set.through
    max_num = 1

    verbose_name_plural = "تخفیف بدون کد"
    verbose_name = "تخفیف بدون کد"

    def get_queryset(self, request):
        qs = super(DiscountWithoutCodeInline, self).get_queryset(request)
        return qs.filter(discount__code__isnull=True)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(DiscountWithoutCodeInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        if db_field.name == 'discount':
            field.limit_choices_to = {'code__isnull': "True"}
        return field


class InstallmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['course', 'get_start_date_decorated', 'get_end_date_decorated','title' , 'amount' ]
    search_fields = ['course','title']


    def get_start_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.start_date).strftime('%y/%m/%d ')

    def get_end_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.end_date).strftime('%y/%m/%d ')

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'


class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ['purchaser_link', 'amount', 'is_successful', 'submit_date_decorated', 'payment_code',
                    'get_installments']
    fields = (
        'purchaser', 'amount', 'is_successful', 'submit_date_decorated', 'payment_code', 'get_installments')
    exclude = ['courses', ]
    readonly_fields = ('purchaser_link',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def purchaser_link(self, obj):
        return mark_safe('<a href="{0}">{1}</a>'.format(
            reverse("admin:accounts_user_change", args=(obj.purchaser.pk,)),
            obj.purchaser
        ))


class CourseDiscountInline(TabularInlineJalaliMixin, admin.TabularInline):
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


class DiscountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['code', 'title', 'percent', 'get_start_date_decorated', 'get_end_date_decorated']
    search_fields = ['code', 'title']
    form = DiscountForm
    inlines = [
        CourseDiscountInline
    ]

    def get_queryset(self, request):
        return Discount.objects.filter(code__isnull=False)

    def get_start_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.start_date).strftime('%y/%m/%d , %H:%M:%S')

    def get_end_date_decorated(self, obj):
        if obj.end_date:
            return jdatetime.datetime.fromgregorian(datetime=obj.end_date).strftime('%y/%m/%d , %H:%M:%S')
        return ""

    get_start_date_decorated.short_description = 'تاریخ شروع'
    get_start_date_decorated.admin_order_field = 'start_date'
    get_end_date_decorated.short_description = 'تاریخ پایان'
    get_end_date_decorated.admin_order_field = 'end_date'


class CourseDiscountWithoutCodeInline(CourseDiscountInline):
    formset = CourseDiscountWithoutCodeFormSet


class DiscountWithoutCodeAdmin(DiscountAdmin):
    form = DiscountWithoutCodeForm
    inlines = [
        CourseDiscountWithoutCodeInline
    ]

    def get_queryset(self, request):
        return Discount.objects.filter(code__isnull=True)



admin.site.register(Pay_History, PayHistoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountWithoutCode, DiscountWithoutCodeAdmin)
admin.site.register(Installment, InstallmentAdmin)