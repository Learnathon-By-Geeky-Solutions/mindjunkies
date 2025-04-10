from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from mindjunkies.courses.models import Course, Module

from .forms import ForumCommentForm, ForumReplyForm, ForumTopicForm
from .models import Course, ForumComment, ForumTopic, Reply

from django.http import HttpResponse
from django.template.loader import render_to_string
class CourseContextMixin:
    """
    Mixin to add the course object to the context based on `course_slug`.
    """

    def get_course(self):
        return get_object_or_404(
            Course.objects.prefetch_related("modules"),
            slug=self.kwargs.get("course_slug"),
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

    def get_module(self):
        return get_object_or_404(
            Module.objects.prefetch_related("forum_posts"),
            id=self.kwargs.get("module_id"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.get_module().forum_posts.all())
        context["module"] = self.get_module()
        course_slug = self.kwargs.get("course_slug")
        context["form"] = ForumTopicForm(course_slug=course_slug)

        return context


class ForumThreadDetailsView(LoginRequiredMixin, CourseContextMixin, TemplateView):
    template_name = "forums/forum_thread_details.html"

    def get_topic(self):
        return get_object_or_404(ForumTopic, slug=self.kwargs.get("topic_slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = self.get_topic()
        context["commentForm"] = ForumCommentForm()
        context["replyForm"] = ForumReplyForm()

        return context


class TopicSubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        module_id = self.kwargs.get("module_id", "")
        course = get_object_or_404(Course, slug=course_slug)

        form = ForumTopicForm(request.POST, course_slug=course_slug)
        if form.is_valid():
            forum_topic = form.save(commit=False)
            forum_topic.author = request.user
            forum_topic.course = course
            forum_topic.save()
            messages.success(request, "Your topic was posted successfully!")
            return redirect(
                "forum_thread", course_slug=course_slug, module_id=module_id
            )

        messages.error(request, "There was an error posting your topic.")
        return redirect("forum_thread", course_slug=course_slug, module_id=module_id)


# mindjunkies/forums/views.py


class CommentSubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        topic_slug = self.kwargs.get("topic_slug")

        content = request.POST.get("content")

        if not topic_slug or not content:
            messages.error(request, "Missing required fields for reply.")
            return redirect(
                "forum_thread_details", course_slug=course_slug, topic_slug=topic_slug
            )

        topic = get_object_or_404(ForumTopic, slug=topic_slug)
        comment = ForumComment(topic=topic, author=request.user, content=content)

        comment.save()
        return redirect(
            "forum_thread_details", course_slug=course_slug, topic_slug=topic_slug
        )


class ReplySubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        comment_id = self.kwargs.get("comment_id")
        topic_slug = self.kwargs.get("topic_slug")

        body = request.POST.get("body", "").strip()  # Ensure it's not None or empty

        if not body:  # If body is empty, return an error
            messages.error(request, "Reply cannot be empty.")
            return redirect(
                "forum_thread_details", course_slug=course_slug, topic_slug=topic_slug
            )

        comment = get_object_or_404(ForumComment, id=comment_id)
        comment = Reply(parent_comment=comment, author=request.user, body=body)

        comment.save()
        return redirect(
            "forum_thread_details", course_slug=course_slug, topic_slug=topic_slug
        )


class ReplyFormView(LoginRequiredMixin, CourseContextMixin, View):
    def get(self, request, *args, **kwargs):
        reply_id = self.kwargs.get("reply_id")
        print(f"Reply ID received: {reply_id}")
        reply = get_object_or_404(Reply, id=reply_id)
        if not reply:
            reply = get_object_or_404(ForumComment, id=reply_id)
        replyForm = ForumReplyForm()

        context = {
            "reply": reply,
            "replyForm": replyForm,
        }
        return render(request, "forums/reply_form.html", context)

    def post(self, request, *args, **kwargs):

        reply_id = self.kwargs.get("reply_id")
        reply = get_object_or_404(Reply, id=reply_id)
        replyForm = ForumReplyForm(request.POST)

        if replyForm.is_valid():
            new_reply = replyForm.save(commit=False)
            new_reply.author = request.user  # Assuming replies are linked to a user
            new_reply.parent_reply = reply  # Assuming a reply can have a parent reply
            new_reply.save()
            return render(request, "forums/reply.html", {"reply": new_reply})

        context = {
            "reply": reply,
            "replyForm": replyForm,
        }
        return render(request, "forums/reply_form.html", context)
    
class LikeToggleView(LoginRequiredMixin, View):
    """Base view for toggling likes on objects"""
    model = None
    template_name = None
    context_object_name = None
    
    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get('pk'))
    
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        user_exist = obj.likes.filter(username=request.user.username).exists()
        if user_exist:
            obj.likes.remove(request.user)
        else:
            obj.likes.add(request.user)
        
     
         
        
        context = {self.context_object_name: obj}
        return render(request, self.template_name, context)
    
    # For compatibility with GET requests
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LikePostView(LikeToggleView):
    """View for toggling likes on Post objects"""
    model = ForumTopic
    template_name = 'forums/partials/like_topic.html'
    context_object_name = 'topic'


class LikeCommentView(LikeToggleView):
    """View for toggling likes on Comment objects"""
    model = ForumComment
    template_name = 'forums/partials/like_comment.html'
    context_object_name = 'comment'


class LikeReplyView(LikeToggleView):
    """View for toggling likes on Reply objects"""
    model = Reply
    template_name = 'forums/partials/like_reply.html'
    context_object_name = 'reply'
      







   

            
            
        
        
