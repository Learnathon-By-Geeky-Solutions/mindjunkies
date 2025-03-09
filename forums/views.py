from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from courses.models import Course
from .models import ForumTopic

class ForumHomeView(LoginRequiredMixin, TemplateView):
    template_name = "forums/forum_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get course_slug from URL
        course_slug = self.kwargs.get('course_slug', '')
        context['course_slug'] = course_slug

        if not course_slug:
            context['error_message'] = "Course slug is missing."
            return context

        # Fetch the course object
        course = get_object_or_404(Course, slug=course_slug)
        context['course'] = course

        # Get all forum topics for the course
        forum_topics = ForumTopic.objects.filter(course=course).select_related('author').prefetch_related('replies', 'replies__author')
        context['forum_topics'] = forum_topics

        return context
