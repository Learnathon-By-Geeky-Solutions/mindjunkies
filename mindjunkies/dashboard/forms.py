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
        widgets = {
            "portfolio_links": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "important_links": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "experience": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "social_media": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

