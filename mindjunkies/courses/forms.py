from cloudinary.forms import CloudinaryFileField
from django import forms
from django.utils.text import slugify

from .models import Course, CourseToken


class CourseForm(forms.ModelForm):
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Enter each requirement in a new line.",
    )
    learning_objectives = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Enter each objective in a new line.",
    )
    course_image = CloudinaryFileField()

    class Meta:
        model = Course
        fields = [
            "title",
            "short_introduction",
            "course_description",
            "category",
            "requirements",
            "learning_objectives",
            "level",
            "course_image",
            "preview_video",
            "upcoming",
            "published",
            "paid_course",
            "course_price",
        ]

    def save(self, commit=True, teacher=None):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)
        if teacher:
            instance.teacher = teacher
        if commit:
            instance.save()
        return instance


class CourseTokenForm(forms.ModelForm):
    class Meta:
        model = CourseToken
        fields = ['course']  # Only allow selecting a course; status & user are handled automatically.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = "Select a course"
        self.fields['course'].widget.attrs.update({
            'class': 'block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500 focus:border-blue-500',
        })


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
