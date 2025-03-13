from django import forms
from .models import Lecture, LecturePDF, LectureVideo
from django.utils.text import slugify
from mindjunkies.courses.models import Module
import os


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'learning_objective', 'order']

        def save(self, commit=True):
            instance = super(LectureForm, self).save(commit=False)
            instance.slug = slugify(instance.title)
            if commit:
                instance.save()

            return instance


class LecturePDFForm(forms.ModelForm):
    class Meta:
        model = LecturePDF
        fields = ['pdf_file', 'pdf_title']

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get("pdf_file")

        if pdf_file:
            # Validate file extension
            ext = os.path.splitext(pdf_file.name)[1].lower()
            if ext != ".pdf":
                raise forms.ValidationError("Only PDF files are allowed.")

            # Validate file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if pdf_file.size > max_size:
                raise forms.ValidationError("File size must be less than 5MB.")

        return pdf_file

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
        fields = ["video_file", "video_title"]

    def clean_video_file(self):
        video_file = self.cleaned_data.get("video_file")

        if video_file:
            # Validate file extension
            ext = os.path.splitext(video_file.name)[1].lower()
            allowed_extensions = [".mp4", ".avi", ".mov", ".mkv"]
            if ext not in allowed_extensions:
                raise forms.ValidationError("Only video files (.mp4, .avi, .mov, .mkv) are allowed.")

            # # Validate file size (e.g., max 50MB)
            # max_size = 50 * 1024 * 1024  # 50MB
            # if video_file.size > max_size:
            #     raise forms.ValidationError("File size must be less than 50MB.")

        return video_file


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']

        def save(self, commit=True):
            instance = super(ModuleForm, self).save(commit=False)
            instance.slug = slugify(instance.title)
            if commit:
                instance.save()

            return instance
