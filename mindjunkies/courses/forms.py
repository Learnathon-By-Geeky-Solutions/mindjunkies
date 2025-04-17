from django import forms
from django.forms import inlineformset_factory

from .models import Course, CourseInfo, CourseToken, Rating

text_area = "form-input mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"

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
            "tags",
        ]
        widgets = {
            "tags": forms.Textarea(
                attrs={
                    "class": text_area,
                    "placeholder": "Enter tags separated by commas (e.g., Python, Django, Web Development)",
                }
            ),
        }

    def clean_intro_video(self):
        intro_video = self.cleaned_data.get('preview_video')
        if intro_video:
            if not intro_video.name.endswith(('mp4', 'mov', 'avi', 'mkv')):
                raise forms.ValidationError("Only video files (mp4, mov, avi, mkv) are allowed.")
        return intro_video


class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ["what_you_will_learn", "who_this_course_is_for", "requirements"]


CourseInfoFormSet = inlineformset_factory(
    Course, CourseInfo, form=CourseInfoForm, extra=1, can_delete=False
)




class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "review"]
