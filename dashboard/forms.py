from accounts.models import User, City, Grade
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'city', 'grades', 'first_name', 'last_name', 'national_code', 'address', 'gender')

    def clean_username(self):
        data = self.cleaned_data['username'].lower()
        return data