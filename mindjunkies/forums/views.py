from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse

from mindjunkies.courses.models import Course, Module

from .forms import ForumCommentForm, ForumReplyForm, ForumTopicForm
from .models import ForumComment, ForumTopic, Reply

from elasticsearch_dsl.query import MultiMatch
from .documents import ForumTopicDocument
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

        module = self.get_module()
        context["module"] = module
        context["posts"] = module.forum_posts.all()
        course_slug = self.kwargs.get("course_slug")
        context["form"] = ForumTopicForm(course_slug=course_slug)
        
        search_query = self.request.GET.get("search")
        print(f"Search query: {search_query}")
        if search_query:
            forumlist = ForumTopicDocument.search().query("match", title=search_query)
            context["posts"] = forumlist.to_queryset()
            print(forumlist.to_queryset())

        return context


class ForumThreadDetailsView(LoginRequiredMixin, CourseContextMixin, TemplateView):
    template_name = "forums/forum_thread_details.html"

    def get_module(self):
        return get_object_or_404(
            Module.objects.prefetch_related("forum_posts"),
            id=self.kwargs.get("module_id"),
        )

    def get_topic(self):
        return get_object_or_404(ForumTopic, id=self.kwargs.get("topic_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = self.get_topic()
        context["commentForm"] = ForumCommentForm()
        context["replyForm"] = ForumReplyForm()
        context["module"] = self.get_module()
        context["form"] = ForumTopicForm(instance=self.get_topic())

        return context


class BaseTopicFormView(LoginRequiredMixin, View):
    """Base class for topic form handling with common functionality"""
    form_class = ForumTopicForm
    success_message = "Operation completed successfully."
    error_message = "There was an error processing your request."

    def get_form_kwargs(self):
        """Get kwargs for form initialization - override in subclasses"""
        return {}

    def get_instance(self):
        """Get the instance for form initialization (None for creation)"""
        return None

    def process_form(self, form, request):
        """Process the form after validation (override in subclasses if needed)"""
        topic = form.save(commit=False)
        return topic

    def get_success_url(self):
        """Override in subclasses to provide the correct redirect URL"""
        raise NotImplementedError("Subclasses must implement get_success_url")

    def post(self, request, *args, **kwargs):
        # Get form instance and kwargs
        instance = self.get_instance()
        form_kwargs = self.get_form_kwargs()

        # Initialize form
        if instance:
            form = self.form_class(request.POST, instance=instance, **form_kwargs)
        else:
            form = self.form_class(request.POST, **form_kwargs)

        # Process form
        if form.is_valid():
            topic = self.process_form(form, request)
            topic.save()
            messages.success(request, self.success_message)
            return redirect(self.get_success_url())

        messages.error(request, self.error_message)
        return redirect(self.get_success_url())


class TopicSubmissionView(BaseTopicFormView):
    """View for creating new topics"""
    success_message = "Your topic was posted successfully!"
    error_message = "There was an error posting your topic."

    def get_form_kwargs(self):
        # Only pass the course_slug that the form expects
        return {"course_slug": self.kwargs.get("course_slug", "")}

    def process_form(self, form, request):
        topic = super().process_form(form, request)
        course_slug = self.kwargs.get("course_slug", "")
        course = get_object_or_404(Course, slug=course_slug)
        topic.author = request.user
        topic.course = course
        return topic

    def get_success_url(self):
        course_slug = self.kwargs.get("course_slug", "")
        module_id = self.kwargs.get("module_id", "")
        return reverse("forum_thread", kwargs={
            "course_slug": course_slug,
            "module_id": module_id
        })


class TopicUpdateView(BaseTopicFormView):
    """View for updating existing topics"""
    success_message = "Topic updated successfully."
    error_message = "There was an error updating your topic."

    def get_instance(self):
        topic_id = self.kwargs.get("topic_id")
        return get_object_or_404(ForumTopic, id=topic_id)

    def get_form_kwargs(self):
        # For update, we don't need to pass course_slug
        return {}

    def get_success_url(self):
        course_slug = self.kwargs.get("course_slug", "")
        module_id = self.kwargs.get("module_id", "")
        topic_id = self.kwargs.get("topic_id")
        return reverse("forum_thread_details", kwargs={
            "course_slug": course_slug,
            "module_id": module_id,
            "topic_id": topic_id
        })


class TopicDeletionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        topic_id = self.kwargs.get("topic_id")
        course_slug = self.kwargs.get("course_slug")
        module_id = self.kwargs.get("module_id")
        topic = get_object_or_404(ForumTopic, id=topic_id)
        topic.delete()
        messages.success(request, "Topic deleted successfully.")
        return redirect(
            "forum_thread", course_slug=course_slug, module_id=module_id
        )


# mindjunkies/forums/views.py


class CommentSubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        topic_id = self.kwargs.get("topic_id")
        module_id = self.kwargs.get("module_id")

        content = request.POST.get("content")

        if not topic_id or not content:
            messages.error(request, "Missing required fields for reply.")
            return redirect(
                "forum_thread_details", course_slug=course_slug, topic_id=topic_id, module_id=module_id
            )

        topic = get_object_or_404(ForumTopic, id=topic_id)
        comment = ForumComment(topic=topic, author=request.user, content=content)

        comment.save()
        return redirect(
            "forum_thread_details", course_slug=course_slug, topic_id=topic_id, module_id=module_id
        )


class CommentDeletionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug")
        topic_id = self.kwargs.get("topic_id")
        module_id = self.kwargs.get("module_id")
        comment_id = self.kwargs.get("comment_id")
        comment = get_object_or_404(ForumComment, id=comment_id)
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("forum_thread_details", topic_id=topic_id, course_slug=course_slug, module_id=module_id)


class ReplySubmissionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug", "")
        comment_id = self.kwargs.get("comment_id")
        topic_id = self.kwargs.get("topic_id")
        module_id = self.kwargs.get("module_id")

        body = request.POST.get("body", "").strip()  # Ensure it's not None or empty

        if not body:  # If body is empty, return an error
            messages.error(request, "Reply cannot be empty.")
            return redirect(
                "forum_thread_details", course_slug=course_slug, topic_id=topic_id, module_id=module_id
            )

        comment = get_object_or_404(ForumComment, id=comment_id)
        comment = Reply(parent_comment=comment, author=request.user, body=body)

        comment.save()
        return redirect(
            "forum_thread_details", course_slug=course_slug, topic_id=topic_id, module_id=module_id
        )


class ReplyDeletionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("course_slug")
        topic_id = self.kwargs.get("topic_id")
        module_id = self.kwargs.get("module_id")
        reply_id = self.kwargs.get("reply_id")
        comment = get_object_or_404(Reply, id=reply_id)
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("forum_thread_details", topic_id=topic_id, course_slug=course_slug, module_id=module_id)


class ReplyFormView(LoginRequiredMixin, CourseContextMixin, View):
    def get(self, request, *args, **kwargs):
        reply_id = self.kwargs.get("reply_id")
        print(f"Reply ID received: {reply_id}")
        reply = get_object_or_404(Reply, id=reply_id)
        if not reply:
            reply = get_object_or_404(ForumComment, id=reply_id)
        reply_form = ForumReplyForm()

        context = {
            "reply": reply,
            "replyForm": reply_form,
        }
        return render(request, "forums/reply_form.html", context)

    def post(self, request, *args, **kwargs):

        reply_id = self.kwargs.get("reply_id")
        reply = get_object_or_404(Reply, id=reply_id)
        reply_form = ForumReplyForm(request.POST)

        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.author = request.user  # Assuming replies are linked to a user
            new_reply.parent_reply = reply  # Assuming a reply can have a parent reply
            new_reply.save()
            return render(request, "forums/reply.html", {"reply": new_reply})

        context = {
            "reply": reply,
            "replyForm": reply_form,
        }
        return render(request, "forums/reply_form.html", context)


class LikeToggleView(LoginRequiredMixin, View):
    """Base view for toggling likes on objects"""

    model = None
    template_name = None
    context_object_name = None

    def get_object(self):
        return get_object_or_404(self.model, id=self.kwargs.get("pk"))

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
    template_name = "forums/partials/like_topic.html"
    context_object_name = "topic"


class LikeCommentView(LikeToggleView):
    """View for toggling likes on Comment objects"""

    model = ForumComment
    template_name = "forums/partials/like_comment.html"
    context_object_name = "comment"


class LikeReplyView(LikeToggleView):
    """View for toggling likes on Reply objects"""

    model = Reply
    template_name = "forums/partials/like_reply.html"
    context_object_name = "reply"
