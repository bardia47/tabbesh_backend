from django import forms
from accounts.models import User , City , Grade 

class ProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
    (True, 'پسر'),
    (False, 'دختر'),
    )
    User.city = forms.ModelChoiceField(queryset=City.objects.all() , to_field_name="title" , required=True)
    User.grades = forms.ModelChoiceField(queryset=Grade.objects.all(), to_field_name="title" , required=True)
    User.avatar = forms.ImageField()
    first_name = forms.CharField(max_length=30 , required=True)
    last_name = forms.CharField(max_length=30 , required=True)
    national_code = forms.CharField(max_length=10 , required=True)
    address = forms.CharField(max_length=255 , required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES , required=True)
    phone_number = forms.CharField(max_length=12 , required=True)
    

