from accounts.models import User , City , Grade 
from django import forms


class ProfileForm(forms.ModelForm):

    city = forms.ModelChoiceField(queryset=City.objects.all(), required=True)
    grades = forms.ModelMultipleChoiceField(queryset=Grade.objects.all(), required=True)
    #avatar = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=30 , required=True)
    last_name = forms.CharField(max_length=30 , required=True)
    national_code = forms.CharField(max_length=10 , required=True)
    address = forms.CharField(max_length=255 , required=True)
    gender = forms.BooleanField()
    phone_number = forms.CharField(max_length=12 , required=True)

    class Meta :
        model = User
        fields = ('city', 'grades', 'avatar', 'first_name' , 'last_name' , 'national_code' , 'address', 'gender', 'phone_number')
