from django import forms
from .models import Lecture, LecturePDF
from django.utils.text import slugify
from courses.models import Module


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['module','title','description','video_url','content','order']
        def save(self, commit=True):
            instance = super(LectureForm, self).save(commit=False)
            instance.slug = slugify(instance.title)
            if commit:
                instance.save()

            return instance


class LecturePDFForm(forms.ModelForm):
    class Meta:
        model = LecturePDF
        fields = ['pdf_file','pdf_title']

    def save(self, commit=True, lecture=None):
        instance = super().save(commit=False)
        if lecture:
            instance.lecture = lecture  # Link to the existing Lecture
        if commit:
            instance.save()
        return instance

class ModuleForm(forms.ModelForm):
    class Meta:
        model=Module
        fields=['title','order']
        def save(self, commit=True):
            instance = super(ModuleForm, self).save(commit=False)
            instance.slug = slugify(instance.title)
            if commit:
                instance.save()

            return instance


