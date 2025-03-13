from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import LiveClass
from mindjunkies.courses.models import Course
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, View


class LiveClassListView(LoginRequiredMixin, ListView):
    model = LiveClass
    template_name = "live_classes/list_live_classes.html"
    context_object_name = "live_classes"

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        return LiveClass.objects.filter(course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        context['course'] = course
        context['teacher'] = course.teachers.filter(teacher=self.request.user).exists()
        return context


class CreateLiveClassView(LoginRequiredMixin, CreateView):
    model = LiveClass
    template_name = "live_classes/create_live_class.html"
    fields = ['topic', 'scheduled_at', 'duration']

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.instance.course = get_object_or_404(Course, slug=self.kwargs['slug'])
        if LiveClass.objects.filter(teacher=self.request.user, scheduled_at=form.instance.scheduled_at).exists():
            messages.error(self.request, "You already have a class scheduled at this time!")
            return redirect("create_live_class", slug=self.kwargs['slug'])
        messages.success(self.request, "Live class created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("list_live_classes", kwargs={"slug": self.kwargs['slug']})


class JoinLiveClassView(LoginRequiredMixin, View):
    """Render a Jitsi meeting inside LMS with JWT authentication."""

    def get(self, request, meeting_id):
        live_class = get_object_or_404(LiveClass, meeting_id=meeting_id)
        return render(request, "live_classes/join_live_class.html", {"live_class": live_class})
