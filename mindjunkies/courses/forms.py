from django import forms
from django.forms import inlineformset_factory

from .models import Course, CourseInfo, CourseToken, Rating


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "short_introduction",
            "course_description",
            "level",
            "category",
            "course_image",
            "published",
            "paid_course",
            "course_price",
            "upcoming",
            "preview_video",
        ]


class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ["what_you_will_learn", "who_this_course_is_for", "requirements"]


CourseInfoFormSet = inlineformset_factory(
    Course, CourseInfo, form=CourseInfoForm, extra=1, can_delete=False
)


class CourseTokenForm(forms.ModelForm):
    class Meta:
        model = CourseToken
        fields = [
            "course"
        ]  # Only allow selecting a course; status & user are handled automatically.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].empty_label = "Select a course"
        self.fields["course"].widget.attrs.update(
            {
                "class": "block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring "
                "focus:ring-blue-500 focus:border-blue-500",
            }
        )


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "review"]
