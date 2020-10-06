from django import forms
from core.utils import Utils


class CourseCalendarFormSetInline(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    if not form.cleaned_data["DELETE"]:
                        count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError("زمان برگذاری برای دوره تعریف نشده است")


class CourseForm(forms.ModelForm):
    def clean_image(self):
        data = self.cleaned_data['image']
        try:
            if self.files['image']:
                data = Utils.compressImage(data,width=500)
                if not self.instance.image.url.startswith("/media/defaults"):
                    self.instance.image.delete()
        except:
            pass
        return data
