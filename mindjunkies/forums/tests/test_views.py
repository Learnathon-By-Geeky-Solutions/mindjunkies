<<<<<<< HEAD
from django.test import TestCase, Client
=======
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
>>>>>>> refactor/dashboard
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from mindjunkies.courses.models import Course, Module
<<<<<<< HEAD
from mindjunkies.forums.models import ForumTopic, ForumComment, Reply, LikedPost, LikedComment, LikedReply
from mindjunkies.forums.views import (
    ForumHomeView, ForumThreadView, ForumThreadDetailsView,
    TopicSubmissionView, TopicUpdateView, TopicDeletionView,
    CommentSubmissionView, CommentDeletionView,
    ReplySubmissionView, ReplyDeletionView, ReplyFormView,
    LikePostView, LikeCommentView, LikeReplyView
)
from django.conf import settings
class ForumTests(TestCase):
=======
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


class TestCourseContextMixin(TestCase):
>>>>>>> refactor/dashboard
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
<<<<<<< HEAD
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
       
        
        # Create a Course with a teacher
=======

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


class TestForumThreadView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
>>>>>>> refactor/dashboard
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            teacher=self.user,  # Assign the user as the teacher
            short_introduction='Test introduction',  # Required field
            course_description='Test description',  # Required field
            level='beginner',  # Required field
            course_price=0.00,  # Required field
        )
        self.module = Module.objects.create(
            course=self.course,
            title='Test Module'
        )
        
        self.topic = ForumTopic.objects.create(
            title='Test Topic',
            content='Test content',
            author=self.user,
            course=self.course,
<<<<<<< HEAD
            module=self.module
=======
            module=self.module,
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
        self.assertEqual(response.status_code, 302)  # Redirect on success


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

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = TopicUpdateView.as_view()
        response = view(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
        )

        # Check that the topic was updated
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, "Updated Topic")
        self.assertEqual(self.topic.content, "Updated content")
        self.assertEqual(response.status_code, 302)  # Redirect on success


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

    def test_post(self):
        """Test topic deletion"""
        request = self.factory.post("/")
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = TopicDeletionView.as_view()
        response = view(
            request,
            course_slug=self.course.slug,
            module_id=self.module.id,
            topic_id=self.topic.id,
        )

        # Check that the topic was deleted
        self.assertEqual(ForumTopic.objects.count(), 0)
        self.assertEqual(response.status_code, 302)  # Redirect on success


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
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
        )

        # Check that a new comment was created
        self.assertEqual(ForumComment.objects.count(), 1)
        comment = ForumComment.objects.first()
        self.assertEqual(comment.content, "Test comment content")
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.topic, self.topic)
        self.assertEqual(response.status_code, 302)  # Redirect on success


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

    def test_post(self):
        """Test comment deletion"""
        request = self.factory.post("/")
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = CommentDeletionView.as_view()
        response = view(
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
            comment_id=self.comment.id,
        )

        # Check that the comment was deleted
        self.assertEqual(ForumComment.objects.count(), 0)
        self.assertEqual(response.status_code, 302)  # Redirect on success


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
>>>>>>> refactor/dashboard
        )
        
        self.comment = ForumComment.objects.create(
<<<<<<< HEAD
            topic=self.topic,
            content='Test comment',
            author=self.user
=======
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
            topic_id=self.topic.id,
            module_id=self.module.id,
            comment_id=self.comment.id,
        )

        # Check that a new reply was created
        self.assertEqual(Reply.objects.count(), 1)
        reply = Reply.objects.first()
        self.assertEqual(reply.body, "Test reply body")
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.parent_comment, self.comment)
        self.assertEqual(response.status_code, 302)  # Redirect on success


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
>>>>>>> refactor/dashboard
        )
        
        self.reply = Reply.objects.create(
            parent_comment=self.comment,
            body='Test reply',
            author=self.user
        )
  

<<<<<<< HEAD
    def test_forum_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_home', kwargs={'course_slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/forum_home.html')
        self.assertEqual(response.context['course'], self.course)

    def test_forum_home_view_unauthenticated(self):
        url = reverse('forum_home', kwargs={'course_slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_forum_thread_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_thread', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/forum_threads.html')
        self.assertEqual(response.context['module'], self.module)
        self.assertIn(self.topic, response.context['posts'])

    def test_forum_thread_view_search(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_thread', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id
        }) + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.topic, response.context['posts'])

    def test_forum_thread_details_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_thread_details', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/forum_thread_details.html')
        self.assertEqual(response.context['topic'], self.topic)
        self.assertEqual(response.context['module'], self.module)

    def test_topic_submission_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_thread', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id
        })
        data = {
            'title': 'New Topic',
            'content': 'New content'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(ForumTopic.objects.filter(title='New Topic').exists())

    def test_topic_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('topic_update', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id
        })
        data = {
            'title': 'Updated Topic',
            'content': 'Updated content'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, 'Updated Topic')

    def test_topic_deletion_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('topic_delete', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ForumTopic.objects.filter(id=self.topic.id).exists())

    def test_comment_submission_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_thread_details', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id
        })
        data = {'content': 'New comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ForumComment.objects.filter(content='New comment').exists())

    def test_comment_deletion_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('comment_delete', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id,
            'comment_id': self.comment.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ForumComment.objects.filter(id=self.comment.id).exists())

    def test_reply_submission_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('forum_thread_details', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id
        })
        data = {'body': 'New reply'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reply.objects.filter(body='New reply').exists())

    def test_reply_deletion_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('reply_delete', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id,
            'reply_id': self.reply.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_reply_form_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('reply_form', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id,
            'reply_id': self.reply.id
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/reply_form.html')
        self.assertEqual(response.context['reply'], self.reply)

    def test_reply_form_view_post(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('reply_form', kwargs={
            'course_slug': self.course.slug,
            'module_id': self.module.id,
            'topic_id': self.topic.id,
            'reply_id': self.reply.id
        })
        data = {'body': 'New nested reply'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/reply.html')
        self.assertTrue(Reply.objects.filter(body='New nested reply').exists())

    def test_like_post_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('like_post', kwargs={'pk': self.topic.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(LikedPost.objects.filter(topic=self.topic, user=self.user).exists())
        
        # Test unlike
        response = self.client.post(url)
        self.assertFalse(LikedPost.objects.filter(topic=self.topic, user=self.user).exists())

    def test_like_comment_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('like_comment', kwargs={'pk': self.comment.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(LikedComment.objects.filter(comment=self.comment, user=self.user).exists())

    def test_like_reply_view(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('like_reply', kwargs={'pk': self.reply.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(LikedReply.objects.filter(reply=self.reply, user=self.user).exists())

    def test_forum_topic_model(self):
        self.assertEqual(str(self.topic), 'Test Topic')
        self.assertEqual(self.topic.slug, slugify('Test Topic'))
        self.assertEqual(self.topic.get_reply_count(), 1)
        self.assertEqual(self.topic.get_last_activity(), max(self.comment.created_at, self.topic.updated_at))

    def test_forum_comment_model(self):
        self.assertEqual(str(self.comment), f"Reply by {self.user.username} on {self.topic.title}")

    def test_reply_model(self):
        self.assertEqual(str(self.reply), f"{self.user.username} : {self.reply.body[:30]}")
=======
    def test_post(self):
        """Test reply deletion"""
        request = self.factory.post("/")
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        view = ReplyDeletionView.as_view()
        response = view(
            request,
            course_slug=self.course.slug,
            topic_id=self.topic.id,
            module_id=self.module.id,
            reply_id=self.reply.id,
        )

        # Check that the reply was deleted
        self.assertEqual(Reply.objects.count(), 0)
        self.assertEqual(response.status_code, 302)  # Redirect on success

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

    def test_get(self):
        request = self.factory.get(f"/forums/{self.course.slug}/reply/{self.reply.id}/")
        request.user = self.user

        view = ReplyFormView.as_view()
        response = view(request, reply_id=self.reply.id, course_slug=self.course.slug)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="body"')  # Check for form input field
         
       

    def test_post_valid_form(self):
        """Test POST with valid reply form data"""
        request = self.factory.post("/", {"body": "New reply body"})
        request.user = self.user

        # Add messages support to request
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        
       

        
        # Updated
        

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

    def test_like_post_view(self):
        """Test LikePostView toggles likes on a topic"""
        request = self.factory.post("/")
        request.user = self.user

        view = LikePostView.as_view()
        response = view(request, pk=self.topic.id)

        # Check that the topic was liked
        self.assertTrue(self.topic.likes.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 200)

        # Test unliking
        response = view(request, pk=self.topic.id)
        self.assertFalse(self.topic.likes.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 200)

    def test_like_comment_view(self):
        """Test LikeCommentView toggles likes on a comment"""
        request = self.factory.post("/")
        request.user = self.user

        view = LikeCommentView.as_view()
        response = view(request, pk=self.comment.id)

        # Check that the comment was liked
        self.assertTrue(self.comment.likes.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 200)

        # Test unliking
        response = view(request, pk=self.comment.id)
        self.assertFalse(self.comment.likes.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 200)

    def test_like_reply_view(self):
        """Test LikeReplyView toggles likes on a reply"""
        request = self.factory.post("/")
        request.user = self.user

        view = LikeReplyView.as_view()
        response = view(request, pk=self.reply.id)

        # Check that the reply was liked
        self.assertTrue(self.reply.likes.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 200)

        # Test unliking
        response = view(request, pk=self.reply.id)
        self.assertFalse(self.reply.likes.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, 200)
>>>>>>> refactor/dashboard
