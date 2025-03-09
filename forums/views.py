from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from courses.models import Course
from .models import ForumTopic,ForumReply

class ForumHomeView(LoginRequiredMixin, TemplateView):
    template_name = "forums/forum_home.html"

    def get_context_data(self, **kwargs):
        # Call the parent class to get the base context
        context = super().get_context_data(**kwargs)
        
        # Get the course_slug from the URL kwargs
        course_slug = self.kwargs.get('course_slug', '')  # Default to empty string if not found

        if not course_slug:
            # If course_slug is empty, handle it (e.g., raise an error or show a message)
            context['error_message'] = "Course slug is missing."
        else:
            # Get the course object using the slug
            course = get_object_or_404(Course, slug=course_slug)
            context['course'] = course
        
        # Pass the course_slug and any other needed context to the template
        context['course_slug'] = course_slug
        
        return context
