from django import forms
from django.utils.text import slugify
from cloudinary.forms import CloudinaryFileField

from .models import Course, CourseTeacher, CourseRequirement, CourseObjective


class CourseForm(forms.ModelForm):
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter each requirement in a new line."
    )
    learning_objectives = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter each objective in a new line."
    )
    course_image = CloudinaryFileField()

    class Meta:
        model = Course
        fields = ['title', 'short_introduction', 'course_description',
                  'requirements', 'learning_objectives', 'level',
                  'course_image', 'preview_video_link',
                  'upcoming', 'published', 'paid_course',
                  'course_price']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CourseForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
            CourseRequirement.objects.filter(course=instance).delete()
            CourseObjective.objects.filter(course=instance).delete()

            for req in self.cleaned_data['requirements'].split('\n'):
                if req.strip():
                    CourseRequirement.objects.create(course=instance, requirement=req)

            for obj in self.cleaned_data['learning_objectives'].split('\n'):
                if obj.strip():
                    CourseObjective.objects.create(course=instance, objective=obj)

        return instance


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)


