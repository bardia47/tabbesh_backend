import jdatetime
from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from accounts.forms import UserForm
from accounts.models import User, Grade, City
from dashboard.models import Installment


class InstallmentInline(admin.TabularInline):
    model = Installment.users.through
    autocomplete_fields = ('installment',)

class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active')
  #  autocomplete_fields = ('installment_set',)
    #readonly_fields=('installment_set',)

    list_filter = ('is_active',)
    form = UserForm
    fields = ('password1', 'password2',
              'first_name', 'last_name', 'avatar', 'gender', 'description', 'is_active', 'phone_number'
              ,'role', 'city',)
    inlines = (InstallmentInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Grade)
admin.site.register(City)
