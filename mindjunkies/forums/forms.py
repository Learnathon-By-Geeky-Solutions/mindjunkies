from django import forms
from django.utils.text import slugify

from .models import ForumReply, ForumTopic


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ["title", "content"]

    def save(self, commit=True):
        instance = super(ForumTopicForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ["content"]
