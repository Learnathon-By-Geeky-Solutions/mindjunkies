from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from mindjunkies.courses.models import Course

from .forms import ForumReplyForm, ForumTopicForm
from .models import ForumReply, ForumTopic


from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Course, ForumTopic
from .forms import ForumTopicForm, ForumReplyForm


class CourseContextMixin:
    """
    Mixin to add the course object to the context based on `course_slug`.
    """
    def get_course(self):
        return get_object_or_404(
            Course.objects.prefetch_related("modules"),
            slug=self.kwargs.get("course_slug")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.get_course()
        return context


class ForumHomeView(LoginRequiredMixin, CourseContextMixin, TemplateView):
    template_name = "forums/forum_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = context["course"]
       

        return context


class ForumThreadView(LoginRequiredMixin, CourseContextMixin, TemplateView):
    template_name = "forums/forum_threads.html"

class ForumThreadDetailsView(LoginRequiredMixin, CourseContextMixin, TemplateView):
    template_name = "forums/forum_thread_details.html"      

class TopicSubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        course = get_object_or_404(Course, slug=course_slug)
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            forum_topic = form.save(commit=False)
            forum_topic.author = request.user
            forum_topic.course = course
            forum_topic.save()
            messages.success(request, "Your topic was posted successfully!")
            return redirect("forum_home", course_slug=course_slug)

        messages.error(request, "There was an error posting your topic.")
        return redirect("forum_home", course_slug=course_slug)


# mindjunkies/forums/views.py


class ReplySubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        topic_id = request.POST.get("topic_id")
        parent_reply_id = request.POST.get("parent_reply_id")
        content = request.POST.get("content")

        if not topic_id or not content:
            messages.error(request, "Missing required fields for reply.")
            return redirect("forum_home", course_slug=course_slug)

        topic = get_object_or_404(ForumTopic, id=topic_id)
        reply = ForumReply(topic=topic, author=request.user, content=content)

        if parent_reply_id:
            parent_reply = get_object_or_404(ForumReply, id=parent_reply_id)
            reply.parent_reply = parent_reply

        reply.save()
        return redirect("forum_home", course_slug=course_slug)


# mindjunkies/forums/views.py


class ReactionSubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        print("Course slug: ", course_slug)
        topic_id = request.POST.get("topic_id")
        topic = get_object_or_404(ForumTopic, id=topic_id)

        if topic.reaction.filter(email=request.user.email).exists():
            topic.reaction.remove(request.user)
        else:
            topic.reaction.add(request.user)

        topic.save()
        return render(
            request,
            "forums/partials/like_button.html",
            context={"course": topic.course, "topic": topic},
        )