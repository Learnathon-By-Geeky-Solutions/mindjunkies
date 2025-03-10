from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from courses.models import Course
from .models import ForumTopic
from .forms import ForumTopicForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ForumTopicForm
from .models import Course, ForumTopic
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


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

        # Initialize the form
        context['form'] = ForumTopicForm()

        return context

    def post(self, request, *args, **kwargs):
        # Get course_slug from URL
        course_slug = self.kwargs.get('course_slug', '')
        course = get_object_or_404(Course, slug=course_slug)

        form = ForumTopicForm(request.POST)
        if form.is_valid():
            forum_topic = form.save(commit=False)
            forum_topic.author = request.user
            forum_topic.course = course
            forum_topic.save()
            messages.success(request, "Your topic was posted successfully!")
            return redirect('forum_home', course_slug=course_slug)  # Redirect to the same page after successful post

        # If form is not valid, return with errors and topics
        forum_topics = ForumTopic.objects.filter(course=course)
        return self.render_to_response(self.get_context_data(
            course=course,
            forum_topics=forum_topics,
            form=form
        ))





