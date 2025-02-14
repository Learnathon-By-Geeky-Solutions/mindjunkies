from django import forms
from django.utils.text import slugify

from .models import Classroom, ClassroomTeacher


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['title', 'short_introduction', 'course_description', 
                  'course_image', 'preview_video_link',
                  'upcoming', 'paid_course',
                  'course_price']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ClassroomForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ClassroomForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
            if self.user:
                ClassroomTeacher.objects.create(classroom=instance, teacher=self.user, role='teacher')
        return instance


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
