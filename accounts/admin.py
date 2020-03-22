from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.hashers import make_password
from .models import *

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email','role')
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        password=make_password(self.cleaned_data["password1"])
        user.password=password
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password',required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','role','email','city', 'grades', 'avatar', 'first_name' , 'last_name' , 'national_code' , 'address', 'gender', 'phone_number')

    def clean_password2(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if self.data.get("password1")!='':
            password=make_password(self.cleaned_data["password1"])
            user.password=password
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_active')
    fieldsets = (
        (None, {'fields': ('username','email',)}),
        ('در صورت نیاز رمز جدید را وارد کنید', {'fields': ('password1','password2',)}),
        ('اطلاعات شخص', {'fields': ('first_name','last_name','avatar','grades','national_code','phone_number')}),
        ('دسترسی ها', {'fields': ('is_superuser','is_active','is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1','password2' )}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(City)
admin.site.register(Grade)
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Course_Calendar)







