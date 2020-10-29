from django.contrib.auth.hashers import make_password
from .models import *
from accounts.enums import RoleCodes
from core.utils import ImageUtils
from django import forms


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

        if self.data.get("password1") is not None and self.data.get("password1") != '':
            password = make_password(self.cleaned_data["password1"])
            user.password = password
        user.set_default_avatar()
        if commit:
            user.save()
        return user

    def clean_avatar(self):
        data = self.cleaned_data['avatar']
        try:
            if self.files['avatar']:
                data = ImageUtils.renameAndCompressImage(data, self.cleaned_data['username'],width=250)
                if not self.instance.avatar.url.startswith("/media/defaults"):
                    self.instance.avatar.delete()
        except:
            pass
        return data


class UserChangeForm(UserCreationForm):
    password1 = forms.CharField(label='رمز', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز', required=False, widget=forms.PasswordInput)
