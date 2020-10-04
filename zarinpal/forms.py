from django.contrib.auth.hashers import make_password
from accounts.models import *
from accounts.enums import RoleCodes, AdminEnums

from django import forms


class InstallmentUserInlineForm(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(InstallmentUserInlineForm, self).__init__(*args, **kwargs)
        self.form.base_fields['installment'].label = "قسط"
        widget = self.form.base_fields['installment'].widget
        widget.label = "قسط"

class CourseDiscountInlineForm(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CourseDiscountInlineForm, self).__init__(*args, **kwargs)
        self.form.base_fields['course'].label = "دوره"
        widget = self.form.base_fields['course'].widget
        widget.label = "دوره"

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('title', 'code', 'percent', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        self.fields['code'].required = True

class DiscountWithoutCodeForm(forms.ModelForm):
    title = forms.CharField(required=True, label="نام تخفیف")

    class Meta:
        model = DiscountWithoutCode
        fields = ('title', 'percent', 'start_date', 'end_date')


class CourseDiscountWithoutCodeFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        discount_id = None
        for form in self.forms:
            if not form.errors and form.is_valid and form.cleaned_data and not form.cleaned_data.get('DELETE'):
                discount_id = form.cleaned_data['discount'].id
                discount = Discount.objects.filter(courses__id=form.cleaned_data['course'].id,
                                                   code__isnull=True).exclude(id=discount_id)
                count = count + 1
                if discount:
                    raise forms.ValidationError("درس " + form.cleaned_data['course'].title + " دارای تخفیف میباشند")
            elif form.cleaned_data.get('DELETE'):
                discount_id = form.cleaned_data['discount'].id
        if count > 0:
            discount = Discount.objects.filter(courses=None, code__isnull=True).exclude(id=discount_id)
            if discount:
                raise forms.ValidationError("تمامی دروس دارای تخفیف میباشند")
        else:
            discount = Discount.objects.filter(~Q(courses=None), code__isnull=True)
            if discount_id is not None:
                discount = discount.exclude(id=discount_id)
            if discount:
                raise forms.ValidationError("برخی دروس دارای تخفیف میباشند")

