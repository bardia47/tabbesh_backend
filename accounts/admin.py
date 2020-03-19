from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(City)
admin.site.register(Grade)
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Course_Calendar)







