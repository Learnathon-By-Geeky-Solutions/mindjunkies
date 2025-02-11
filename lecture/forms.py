from django import forms
from .models import Lecture # Import your model

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title','pdf_file']
    def save(self, commit=True):
        instance = super(LectureForm, self).save(commit=False)
        instance.slug = instance.title.lower().replace(' ', '-')
        if commit:
            instance.save()
            return instance
        
class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)                