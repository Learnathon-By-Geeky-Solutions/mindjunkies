from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from decouple import config

from mindjunkies.courses.models import Course, Module
from mindjunkies.forums.models import ForumTopic, ForumComment, Reply

User = get_user_model()


class ForumViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user (who will also be the teacher)
        self.user = User.objects.create_user(username="testuser", password=config("TEST_PASS"))

        # Assign this user as a teacher for the course
        self.teacher = User.objects.create_user(username="teacheruser", password=config("TEST_PASS"))

        # Create a course with a teacher
        self.course = Course.objects.create(title="Test Course", slug="test-course", teacher=self.teacher)

        # Create a module linked to the course
        self.module = Module.objects.create(course=self.course, title="Test Module")

        # Create a forum topic assigned to the module
        self.forum_topic = ForumTopic.objects.create(
            title="Test Topic", slug="test-topic", author=self.user, course=self.course, module=self.module
        )

        # Create a comment on the forum topic
        self.comment = ForumComment.objects.create(
            topic=self.forum_topic, author=self.user, content="Test Comment"
        )

        # Create a reply to the comment
        self.reply = Reply.objects.create(
            parent_comment=self.comment, author=self.user, body="Test Reply"
        )

    def test_forum_home_view_requires_login(self):
        response = self.client.get(reverse("forum_home", kwargs={"course_slug": self.course.slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_forum_home_view_authenticated(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.get(reverse("forum_home", kwargs={"course_slug": self.course.slug}))
        self.assertEqual(response.status_code, 200)  # Should render the forum home

    def test_forum_thread_view(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.get(
            reverse("forum_thread", kwargs={"course_slug": self.course.slug, "module_id": self.module.id}))
        self.assertEqual(response.status_code, 200)

    def test_forum_thread_details_view(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.get(reverse("forum_thread_details", kwargs={"course_slug": self.course.slug,
                                                                           "topic_id": self.forum_topic.id}))
        self.assertEqual(response.status_code, 200)

    def test_topic_submission_view(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.post(
            reverse("topic_submission", kwargs={"course_slug": self.course.slug, "module_id": self.module.id}),
            {"title": "New Topic", "content": "Topic Content"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(ForumTopic.objects.filter(title="New Topic").exists())

    def test_comment_submission_view(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.post(
            reverse("comment_submission",
                    kwargs={"course_slug": self.course.slug, "topic_id": self.forum_topic.id}),
            {"content": "New Comment"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(ForumComment.objects.filter(content="New Comment").exists())

    def test_reply_submission_view(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.post(
            reverse("reply_submission", kwargs={"course_slug": self.course.slug, "topic_id": self.forum_topic.id,
                                                "comment_id": self.comment.id}),
            {"body": "New Reply"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Reply.objects.filter(body="New Reply").exists())

    def test_reply_form_view_get(self):
        self.client.login(username="testuser", password=config("TEST_PASS"))
        response = self.client.get(reverse("reply_form", kwargs={"reply_id": self.reply.id}))
        self.assertEqual(response.status_code, 200)
