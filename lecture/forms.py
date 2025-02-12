from django import forms
from django.utils.text import slugify
from .models import Lecture  # Import your model

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'pdf_file']

    def save(self, commit=True):
        # Save the instance without committing to the database immediately
        instance = super().save(commit=False)
        
        # Generate a slug using slugify for better handling
        instance.slug = slugify(instance.title)
        
        if commit:
            instance.save()
        
        return instance
