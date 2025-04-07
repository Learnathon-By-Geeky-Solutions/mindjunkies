from django import forms
from .models import TeacherVerification, Certificate

class TeacherVerificationForm(forms.ModelForm):
    certificates = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}), 
        required=True
    )
    
    class Meta:
        model = TeacherVerification
        fields = ['full_name', 'email', 'phone', 'address', 'portfolio_links', 
                  'important_links', 'experience', 'social_media', 'certificates']
