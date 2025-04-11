import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from mindjunkies.courses.models import Course, Module
from mindjunkies.forums.forms import ForumCommentForm, ForumReplyForm, ForumTopicForm
from mindjunkies.forums.models import ForumComment, ForumTopic, Reply
from mindjunkies.forums.views import (CommentSubmissionView, ForumHomeView, ForumThreadDetailsView, ForumThreadView,
                                      LikeCommentView, LikePostView, LikeReplyView, ReplySubmissionView,
                                      TopicSubmissionView)

User = get_user_model()


@pytest.mark.django_db
class TestCourseContextMixin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )

    def test_get_course(self):
        """Test that get_course returns the correct course based on slug"""
        view = ForumHomeView()
        view.kwargs = {"course_slug": self.course.slug}
        course = view.get_course()

        self.assertEqual(course, self.course)

    def test_get_context_data(self):
        """Test that course is added to context"""
        request = self.factory.get("/")
        request.user = self.user

        view = ForumHomeView()
        view.request = request
        view.kwargs = {"course_slug": self.course.slug}

        context = view.get_context_data()

        self.assertEqual(context["course"], self.course)


@pytest.mark.django_db
class TestForumThreadView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(
            title="Test Module", details="Module details", course=self.course, order=1
        )

    def test_get_module(self):
        """Test that get_module returns the correct module"""
        view = ForumThreadView()
        view.kwargs = {"module_id": self.module.id}
        module = view.get_module()

        self.assertEqual(module, self.module)

    def test_get_context_data(self):
        """Test that module and form are added to context"""
        request = self.factory.get("/")
        request.user = self.user

        view = ForumThreadView()
        view.request = request
        view.kwargs = {"course_slug": self.course.slug, "module_id": self.module.id}

        context = view.get_context_data()

        self.assertEqual(context["module"], self.module)
        self.assertIsInstance(context["form"], ForumTopicForm)


@pytest.mark.django_db
class TestForumThreadDetailsView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(
            title="Test Module", details="Module details", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )

    def test_get_topic(self):
        """Test that get_topic returns the correct topic"""
        view = ForumThreadDetailsView()
        view.kwargs = {"topic_slug": self.topic.slug}
        topic = view.get_topic()

        self.assertEqual(topic, self.topic)

    def test_get_context_data(self):
        """Test that topic and forms are added to context"""
        request = self.factory.get("/")
        request.user = self.user

        view = ForumThreadDetailsView()
        view.request = request
        view.kwargs = {"course_slug": self.course.slug, "topic_slug": self.topic.slug}

        context = view.get_context_data()

        self.assertEqual(context["topic"], self.topic)
        self.assertIsInstance(context["commentForm"], ForumCommentForm)
        self.assertIsInstance(context["replyForm"], ForumReplyForm)


@pytest.mark.django_db
class TestTopicSubmissionView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(
            title="Test Module", details="Module details", course=self.course, order=1
        )

    def test_post_valid_form(self):
        """Test topic submission with valid form data"""
        request = self.factory.post(
            "/",
            {
                "title": "New Topic",
                "content": "Topic content",
                "module": self.module.id,
            },
        )
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = TopicSubmissionView.as_view()
        response = view(request, course_slug=self.course.slug, module_id=self.module.id)

        # Check that a new topic was created
        self.assertEqual(ForumTopic.objects.count(), 1)
        topic = ForumTopic.objects.first()
        self.assertEqual(topic.title, "New Topic")
        self.assertEqual(topic.author, self.user)
        self.assertEqual(topic.course, self.course)
        self.assertEqual(topic.module, self.module)


@pytest.mark.django_db
class TestCommentSubmissionView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(
            title="Test Module", details="Module details", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )

    def test_post_valid_comment(self):
        """Test comment submission with valid data"""
        request = self.factory.post("/", {"content": "Test comment content"})
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = CommentSubmissionView.as_view()
        response = view(
            request, course_slug=self.course.slug, topic_slug=self.topic.slug
        )

        # Check that a new comment was created
        self.assertEqual(ForumComment.objects.count(), 1)
        comment = ForumComment.objects.first()
        self.assertEqual(comment.content, "Test comment content")
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.topic, self.topic)


@pytest.mark.django_db
class TestReplySubmissionView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(
            title="Test Module", details="Module details", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )
        self.comment = ForumComment.objects.create(
            topic=self.topic, author=self.user, content="Test comment"
        )

    def test_post_valid_reply(self):
        """Test reply submission with valid data"""
        request = self.factory.post("/", {"body": "Test reply body"})
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = ReplySubmissionView.as_view()
        response = view(
            request,
            course_slug=self.course.slug,
            topic_slug=self.topic.slug,
            comment_id=self.comment.id,
        )

        # Check that a new reply was created
        self.assertEqual(Reply.objects.count(), 1)
        reply = Reply.objects.first()
        self.assertEqual(reply.body, "Test reply body")
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.parent_comment, self.comment)


@pytest.mark.django_db
class TestLikeViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed course description",
            teacher=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(
            title="Test Module", details="Module details", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )
        self.comment = ForumComment.objects.create(
            topic=self.topic, author=self.user, content="Test comment"
        )
        self.reply = Reply.objects.create(
            parent_comment=self.comment, author=self.user, body="Test reply"
        )

    def test_like_topic(self):
        """Test liking a topic directly"""
        # Directly test the like functionality
        self.topic.likes.add(self.user)
        self.assertTrue(self.topic.likes.filter(username=self.user.username).exists())

        # Test unliking
        self.topic.likes.remove(self.user)
        self.assertFalse(self.topic.likes.filter(username=self.user.username).exists())

    def test_like_comment(self):
        """Test liking a comment directly"""
        # Directly test the like functionality
        self.comment.likes.add(self.user)
        self.assertTrue(self.comment.likes.filter(username=self.user.username).exists())

    def test_like_reply(self):
        """Test liking a reply directly"""
        # Directly test the like functionality
        self.reply.likes.add(self.user)
        self.assertTrue(self.reply.likes.filter(username=self.user.username).exists())
