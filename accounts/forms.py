from django import forms
from .models import City, User


class UserForm(forms.ModelForm):
    # username = forms.CharField(max_length=30)
    # password = forms.CharField(max_length=30)
    # email = forms.EmailField()
    # city = forms.ModelChoiceField(queryset=City.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'city', 'first_name',
                  'last_name', 'grades', 'gender', 'phone_number', 'national_code')
