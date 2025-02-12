from django import forms
from .models import Lecture, LecturePDF

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'classroom']

class LecturePDFForm(forms.ModelForm):
    class Meta:
        model = LecturePDF
        fields = ['pdf_file']

    def save(self, commit=True, lecture=None):
        instance = super().save(commit=False)
        if lecture:
            instance.lecture = lecture  # Link to the existing Lecture
        if commit:
            instance.save()
        return instance
