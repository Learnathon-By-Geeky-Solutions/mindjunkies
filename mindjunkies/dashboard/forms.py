from django import forms
from .models import TeacherVerificationRequest

class TeacherVerificationForm(forms.ModelForm):
    class Meta:
        model = TeacherVerificationRequest
        fields = ["subject", "portfolio_link", "certificates"]

        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded-lg",
                "placeholder": "What do you want to teach?",
                "required": True
            }),
            "portfolio_link": forms.URLInput(attrs={
                "class": "w-full p-2 border rounded-lg",
                "placeholder": "Portfolio or LinkedIn (optional)"
            }),
            "certificates": forms.ClearableFileInput(attrs={
                "class": "w-full p-2 border rounded-lg"
            }),
        }

    def clean_certificates(self):
        certificates = self.cleaned_data.get("certificates")
        if certificates:
            if certificates.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Certificate file size should not exceed 5MB.")
        return certificates
