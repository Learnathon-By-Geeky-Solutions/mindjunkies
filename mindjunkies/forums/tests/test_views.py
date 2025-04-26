import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from mindjunkies.courses.models import Course, Module
from mindjunkies.forums.forms import ForumCommentForm, ForumReplyForm, ForumTopicForm
from mindjunkies.forums.models import ForumComment, ForumTopic, Reply
from mindjunkies.forums.views import (
    CommentDeletionView,
    CommentSubmissionView,
    ForumHomeView,
    ForumThreadDetailsView,
    ForumThreadView,
    LikeCommentView,
    LikePostView,
    LikeReplyView,
    ReplyDeletionView,
    ReplyFormView,
    ReplySubmissionView,
    TopicDeletionView,
    TopicSubmissionView,
    TopicUpdateView,
)

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
class TestForumHomeView(TestCase):
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
            title="Test Module", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )

    def test_get_module(self):
        """Test that get_module returns the correct module"""
        view = ForumThreadView()
        view.kwargs = {"module_id": self.module.id}
        module = view.get_module()
        self.assertEqual(module, self.module)

    def test_get_context_data(self):
        """Test that module, posts, and form are added to context"""
        request = self.factory.get("/")
        request.user = self.user
        view = ForumThreadView()
        view.request = request
        view.kwargs = {"course_slug": self.course.slug, "module_id": self.module.id}
        context = view.get_context_data()
        self.assertEqual(context["module"], self.module)
        self.assertEqual(list(context["posts"]), [self.topic])
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
            title="Test Module", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )

    def test_get_module(self):
        """Test that get_module returns the correct module"""
        view = ForumThreadDetailsView()
        view.kwargs = {"module_id": self.module.id}
        module = view.get_module()
        self.assertEqual(module, self.module)

    def test_get_topic(self):
        """Test that get_topic returns the correct topic"""
        view = ForumThreadDetailsView()
        view.kwargs = {"topic_id": self.topic.id}
        topic = view.get_topic()
        self.assertEqual(topic, self.topic)

    def test_get_context_data(self):
        """Test that topic, forms, and module are added to context"""
        request = self.factory.get("/")
        request.user = self.user
        view = ForumThreadDetailsView()
        view.request = request
        view.kwargs = {
            "course_slug": self.course.slug,
            "module_id": self.module.id,
            "topic_id": self.topic.id,
        }
        context = view.get_context_data()
        self.assertEqual(context["topic"], self.topic)
        self.assertEqual(context["module"], self.module)
        self.assertIsInstance(context["commentForm"], ForumCommentForm)
        self.assertIsInstance(context["replyForm"], ForumReplyForm)
        self.assertIsInstance(context["form"], ForumTopicForm)


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
            title="Test Module", course=self.course, order=1
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
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TopicSubmissionView.as_view()(
            request, course_slug=self.course.slug, module_id=self.module.id
        )
        self.assertEqual(ForumTopic.objects.count(), 1)
        topic = ForumTopic.objects.first()
        self.assertEqual(topic.title, "New Topic")
        self.assertEqual(topic.author, self.user)
        self.assertEqual(topic.course, self.course)
        self.assertEqual(topic.module, self.module)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread",
                kwargs={"course_slug": self.course.slug, "module_id": self.module.id},
            ),
        )

    def test_post_invalid_form(self):
        """Test topic submission with invalid form data"""
        request = self.factory.post(
            "/",
            {"title": "", "content": "", "module": self.module.id},  # Invalid: empty title
        )
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TopicSubmissionView.as_view()(
            request, course_slug=self.course.slug, module_id=self.module.id
        )
        self.assertEqual(ForumTopic.objects.count(), 0)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread",
                kwargs={"course_slug": self.course.slug, "module_id": self.module.id},
            ),
        )


@pytest.mark.django_db
class TestTopicUpdateView(TestCase):
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
            title="Test Module", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )

    def test_get_instance(self):
        """Test that get_instance returns the correct topic"""
        view = TopicUpdateView()
        view.kwargs = {"topic_id": self.topic.id}
        instance = view.get_instance()
        self.assertEqual(instance, self.topic)

    def test_post_valid_form(self):
        """Test topic update with valid form data"""
        request = self.factory.post(
            "/",
            {
                "title": "Updated Topic",
                "content": "Updated content",
                "module": self.module.id,
            },
        )
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TopicUpdateView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
        )
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, "Updated Topic")
        self.assertEqual(self.topic.content, "Updated content")
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )

    def test_post_invalid_form(self):
        """Test topic update with invalid form data"""
        request = self.factory.post(
            "/",
            {"title": "", "content": "", "module": self.module.id},  # Invalid: empty title
        )
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TopicUpdateView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
        )
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, "Test Topic")  # Original title unchanged
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )


@pytest.mark.django_db
class TestTopicDeletionView(TestCase):
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
            title="Test Module", course=self.course, order=1
        )
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            slug="test-topic",
            content="Test Content",
            author=self.user,
            course=self.course,
            module=self.module,
        )

    def test_post(self):
        """Test topic deletion"""
        request = self.factory.post("/")
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = TopicDeletionView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
        )
        self.assertEqual(ForumTopic.objects.count(), 0)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread",
                kwargs={"course_slug": self.course.slug, "module_id": self.module.id},
            ),
        )


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
            title="Test Module", course=self.course, order=1
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
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = CommentSubmissionView.as_view()(
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
        )
        self.assertEqual(ForumComment.objects.count(), 1)
        comment = ForumComment.objects.first()
        self.assertEqual(comment.content, "Test comment content")
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.topic, self.topic)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )

    def test_post_invalid_comment(self):
        """Test comment submission with empty content"""
        request = self.factory.post("/", {"content": ""})
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = CommentSubmissionView.as_view()(
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
        )
        self.assertEqual(ForumComment.objects.count(), 0)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )


@pytest.mark.django_db
class TestCommentDeletionView(TestCase):
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
            title="Test Module", course=self.course, order=1
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

    def test_post(self):
        """Test comment deletion"""
        request = self.factory.post("/")
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = CommentDeletionView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
            comment_id=self.comment.id,
        )
        self.assertEqual(ForumComment.objects.count(), 0)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )


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
            title="Test Module", course=self.course, order=1
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
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = ReplySubmissionView.as_view()(
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
            comment_id=self.comment.id,
        )
        self.assertEqual(Reply.objects.count(), 1)
        reply = Reply.objects.first()
        self.assertEqual(reply.body, "Test reply body")
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.parent_comment, self.comment)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )

    def test_post_invalid_reply(self):
        """Test reply submission with empty body"""
        request = self.factory.post("/", {"body": ""})
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = ReplySubmissionView.as_view()(
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
            comment_id=self.comment.id,
        )
        self.assertEqual(Reply.objects.count(), 0)
        self.assertEqual(
            response.url,
            reverse(
                "forum_thread_details",
                kwargs={
                    "course_slug": self.course.slug,
                    "module_id": self.module.id,
                    "topic_id": self.topic.id,
                },
            ),
        )


@pytest.mark.django_db
class TestReplyDeletionView(TestCase):
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
            title="Test Module", course=self.course, order=1
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

    def test_post(self):
        """Test reply deletion"""
        request = self.factory.post("/")
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = ReplyDeletionView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
            reply_id=self.reply.id,
        )
        self.assertEqual(Reply.objects.count(), 0)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestReplyFormView(TestCase):
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
            title="Test Module", course=self.course, order=1
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

    def test_get(self):
        """Test GET request renders reply form"""
        request = self.factory.get("/")
        request.user = self.user
        response = ReplyFormView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
            reply_id=self.reply.id,
        )
        self.assertEqual(response.status_code, 200)

    def test_post_valid_form(self):
        """Test POST request with valid reply form data"""
        request = self.factory.post("/", {"body": "New reply body"})
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = ReplyFormView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
            reply_id=self.reply.id,
        )
        self.assertEqual(Reply.objects.count(), 2)  # Original + new reply
        new_reply = Reply.objects.exclude(id=self.reply.id).first()
        self.assertEqual(new_reply.body, "New reply body")
        self.assertEqual(new_reply.author, self.user)

    def test_post_invalid_form(self):
        """Test POST request with invalid reply form data"""
        request = self.factory.post("/", {"body": ""})
        request.user = self.user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = ReplyFormView.as_view()(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
            reply_id=self.reply.id,
        )
        self.assertEqual(Reply.objects.count(), 1)  # Only original reply


@pytest.mark.django_db
class TestLikeViews(TestCase):
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
            title="Test Module", course=self.course, order=1
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

    def test_like_post_view(self):
        """Test LikePostView toggles likes on ForumTopic"""
        request = self.factory.post("/")
        request.user = self.user
        response = LikePostView.as_view()(
            request,
            pk=self.topic.id,
        )
        self.assertTrue(self.topic.likes.filter(username=self.user.username).exists())

        # Test unlike
        response = LikePostView.as_view()(
            request,
            pk=self.topic.id,
        )
        self.assertFalse(self.topic.likes.filter(username=self.user.username).exists())

    def test_like_comment_view(self):
        """Test LikeCommentView toggles likes on ForumComment"""
        request = self.factory.post("/")
        request.user = self.user
        response = LikeCommentView.as_view()(
            request,
            pk=self.comment.id,
        )
        self.assertTrue(self.comment.likes.filter(username=self.user.username).exists())

        # Test unlike
        response = LikeCommentView.as_view()(
            request,
            pk=self.comment.id,
        )
        self.assertFalse(self.comment.likes.filter(username=self.user.username).exists())

    def test_like_reply_view(self):
        """Test LikeReplyView toggles likes on Reply"""
        request = self.factory.post("/")
        request.user = self.user
        response = LikeReplyView.as_view()(
            request,
            pk=self.reply.id,
        )
        self.assertTrue(self.reply.likes.filter(username=self.user.username).exists())

        # Test unlike
        response = LikeReplyView.as_view()(
            request,
            pk=self.reply.id,
        )
        self.assertFalse(self.reply.likes.filter(username=self.user.username).exists())
