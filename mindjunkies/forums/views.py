from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from mindjunkies.courses.models import Course

from .forms import ForumReplyForm, ForumTopicForm
from .models import ForumReply, ForumTopic


class ForumHomeView(LoginRequiredMixin, TemplateView):
    template_name = "forums/forum_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get course_slug from URL
        course_slug = self.kwargs.get("course_slug", "")
        context["course_slug"] = course_slug

        if not course_slug:
            context["error_message"] = "Course slug is missing."
            return context

        # Fetch the course object
        course = get_object_or_404(Course, slug=course_slug)
        context["course"] = course

        # Get all forum topics for the course
        forum_topics = (
            ForumTopic.objects.filter(course=course)
            .select_related("author")
            .prefetch_related("replies", "replies__author")
        )
        context["forum_topics"] = forum_topics

        # Initialize the forms
        context["form"] = ForumTopicForm()
        context["reply_form"] = ForumReplyForm()

        return context

    def post(self, request, *args, **kwargs):
        # Get course_slug from URL
        course_slug = self.kwargs.get("course_slug", "")
        course = get_object_or_404(Course, slug=course_slug)

        # Check if this is a topic submission or a reply submission
        if "replies" in request.POST:
            # This is a reply submission
            return self.handle_reply_submission(request, course_slug)
           #This is a react submission
        elif "reaction" in request.POST:
            print("this is saima")
            return self.handle_reaction_submission(request, course_slug)

        else:
            # This is a new topic submission
            return self.handle_topic_submission(request, course, course_slug)

    def handle_topic_submission(self, request, course, course_slug):
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            forum_topic = form.save(commit=False)
            forum_topic.author = request.user
            forum_topic.course = course
            forum_topic.save()
            messages.success(request, "Your topic was posted successfully!")
            return redirect("forum_home", course_slug=course_slug)

        # If form is not valid, return with errors and topics
        forum_topics = ForumTopic.objects.filter(course=course)
        return self.render_to_response(
            self.get_context_data(course=course, forum_topics=forum_topics, form=form)
        )

    def handle_reply_submission(self, request, course_slug):
        topic_id = request.POST.get("topic_id")
        parent_reply_id = request.POST.get("parent_reply_id")
        content = request.POST.get("content")
        print("from reply")

        # Validate required fields
        if not topic_id or not content:
            messages.error(request, "Missing required fields for reply.")
            return redirect("forum_home", course_slug=course_slug)

        # Get the topic
        topic = get_object_or_404(ForumTopic, id=topic_id)

        # Create the reply
        reply = ForumReply(topic=topic, author=request.user, content=content)

        # If parent_reply_id is provided, set the parent reply
        if parent_reply_id:
            parent_reply = get_object_or_404(ForumReply, id=parent_reply_id)
            reply.parent_reply = parent_reply

        reply.save()

        # Redirect back to the forum home with the replies section open
        return HttpResponseRedirect(
            f"{reverse('forum_home', kwargs={'course_slug': course_slug})}#replies-container-{topic_id}"
        )
    def handle_reaction_submission(self, request, course_slug):
        topic_id = request.POST.get("topic_id")
        topic = get_object_or_404(ForumTopic, id=topic_id)
        
        if topic.reaction.filter(email=request.user.email).exists():
            # User is un-reacting
            topic.reaction.remove(request.user)
            # Update like_count
            # topic.like_count = max(0, topic.like_count - 1)  # Ensure it doesn't go below 0
            topic.save()
        else:
            # User is reacting
            topic.reaction.add(request.user)
            # Update like_count
            # topic.like_count += 1
            topic.save()
            
        return HttpResponseRedirect(
            f"{reverse('forum_home', kwargs={'course_slug': course_slug})}"
        )
    
