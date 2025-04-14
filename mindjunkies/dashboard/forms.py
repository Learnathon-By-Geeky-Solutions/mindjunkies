from django import forms

from .models import TeacherVerification


class TeacherVerificationForm(forms.ModelForm):
    class Meta:
        model = TeacherVerification
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "portfolio_links",
            "important_links",
            "experience",
            "social_media",
        ]
