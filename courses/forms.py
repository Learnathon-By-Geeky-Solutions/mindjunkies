from django import forms
from django.utils.text import slugify

from .models import Course, CourseTeacher


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'short_introduction', 'course_description', 
                  'course_image', 'preview_video_link',
                  'upcoming', 'paid_course',
                  'course_price']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CourseForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()

        return instance


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
