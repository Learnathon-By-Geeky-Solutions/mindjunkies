from django import forms
from .models import Classroom # Import your model

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['title', 'short_introduction', 'course_description', 
                  'course_image', 'preview_video_link', 'published', 
                  'upcoming', 'published_on', 'paid_course', 
                  'course_price', 'slug', 'total_rating', 'number_of_ratings']
