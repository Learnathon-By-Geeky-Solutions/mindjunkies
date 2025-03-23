from django import forms
from django.utils.text import slugify

from .models import ForumComment, ForumTopic
from mindjunkies.courses.models import Module,Course
from django.shortcuts import get_object_or_404

class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ["title", "content","module"]

    def __init__(self, *args, **kwargs):
        # Get the course object from kwargs (passed when initializing the form)
        course_slug = kwargs.pop('course_slug', None)
        super().__init__(*args, **kwargs)

        # If course is provided, filter the available modules based on the course
        if course_slug:
            course = get_object_or_404(Course, slug=course_slug)
            self.fields['module'].queryset = Module.objects.filter(course=course)    

    def save(self, commit=True):
        instance = super(ForumTopicForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ["content"]
