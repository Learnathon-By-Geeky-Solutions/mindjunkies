from django import forms
from .models import Lecture, LecturePDF,LectureVideo

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'})  # Fix select field styling
        }

class LecturePDFForm(forms.ModelForm):
    class Meta:
        model = LecturePDF
        fields = ['pdf_file', 'lecture']
        widgets = {
            'lecture': forms.Select(attrs={'class': 'form-select'}),  # Fix select field styling
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'})  # File input styling
        }
        labels = {
            'lecture': 'Module',  # Custom label for the 'title' field
             
        }

    def save(self, commit=True, lecture=None):
        instance = super().save(commit=False)
        if lecture:
            instance.lecture = lecture  # Link to the existing Lecture
        if commit:
            instance.save()
        return instance

class LectureVideoForm(forms.ModelForm):
    class Meta:
        model = LectureVideo
        fields = ['video_file', 'lecture']
        widgets = {
            'lecture': forms.Select(attrs={'class': 'form-select'}),  # Fix select field styling
            'video_file': forms.FileInput(attrs={'class': 'form-control'})  # File input styling
        }
        labels = {
            'lecture': 'Module',  # Custom label for the 'title' field
             
        }

    def save(self, commit=True, lecture=None):
        instance = super().save(commit=False)
        if lecture:
            instance.lecture = lecture  # Link to the existing Lecture
        if commit:
            instance.save()
        return instance    
