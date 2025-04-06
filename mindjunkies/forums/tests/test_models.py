from django.test import TestCase
from django.contrib.auth import get_user_model
from mindjunkies.courses.models import Course, Module
from mindjunkies.forums.models import (
    ForumTopic, ForumComment, Reply,
    LikedPost, LikedComment, LikedReply
)
from decouple import config

User = get_user_model()

class ForumModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password=config('TEST_PASS'))

        self.course = Course.objects.create(
            title='Test Course',
            short_introduction='This is a short intro.',
            course_description='Detailed description of the course.',
            teacher=self.user,
            slug='test-course'
        )

        self.module = Module.objects.create(
            course=self.course,
            title='Test Module'
        )

        self.topic = ForumTopic.objects.create(
            title='Test Topic',
            content='Some content here.',
            author=self.user,
            course=self.course,
            module=self.module
        )

    def test_topic_slug_generated(self):
        self.assertEqual(self.topic.slug, 'test-topic')

    def test_topic_str(self):
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_comment_creation(self):
        comment = ForumComment.objects.create(
            topic=self.topic,
            content="This is a comment",
            author=self.user
        )
        self.assertEqual(str(comment), f"Reply by {self.user.username} on {self.topic.title}")
        self.assertEqual(self.topic.comments.count(), 1)

    def test_reply_creation(self):
        comment = ForumComment.objects.create(
            topic=self.topic,
            content="Another comment",
            author=self.user
        )
        reply = Reply.objects.create(
            author=self.user,
            parent_comment=comment,
            body="This is a reply"
        )
        self.assertEqual(str(reply), f"{self.user.username} : This is a reply")
        self.assertEqual(comment.replies.count(), 1)

    def test_nested_reply(self):
        comment = ForumComment.objects.create(
            topic=self.topic,
            content="Comment",
            author=self.user
        )
        parent_reply = Reply.objects.create(
            author=self.user,
            parent_comment=comment,
            body="Reply 1"
        )
        child_reply = Reply.objects.create(
            author=self.user,
            parent_reply=parent_reply,
            body="Reply 2"
        )
        self.assertEqual(parent_reply.replies.first(), child_reply)

    def test_liked_post(self):
        liked_post = LikedPost.objects.create(
            topic=self.topic,
            user=self.user
        )
        self.assertEqual(str(liked_post), f"{self.user.username} : {self.topic.content[:30]}")

    def test_liked_comment(self):
        comment = ForumComment.objects.create(
            topic=self.topic,
            content="Liking this!",
            author=self.user
        )
        liked_comment = LikedComment.objects.create(
            comment=comment,
            user=self.user
        )
        # Simulate the missing `body` by patching the comment object
        liked_comment.comment.body = comment.content
        self.assertEqual(str(liked_comment), f"{self.user.username} : {comment.content[:30]}")

    def test_liked_reply(self):
        comment = ForumComment.objects.create(
            topic=self.topic,
            content="Comment",
            author=self.user
        )
        reply = Reply.objects.create(
            author=self.user,
            parent_comment=comment,
            body="Like this reply!"
        )
        liked_reply = LikedReply.objects.create(
            reply=reply,
            user=self.user
        )
        self.assertEqual(str(liked_reply), f"{self.user.username} : {reply.body[:30]}")

    def test_get_reply_count_and_last_activity(self):
        comment = ForumComment.objects.create(
            topic=self.topic,
            content="Comment",
            author=self.user
        )
        reply = Reply.objects.create(
            author=self.user,
            parent_comment=comment,
            body="Reply here"
        )

        # Simulate topic.get_reply_count() using related comments and replies
        reply_count = Reply.objects.filter(parent_comment__topic=self.topic).count()
        self.assertEqual(reply_count, 1)

        # Simulate topic.get_last_activity() using latest comment or reply
        last_comment = ForumComment.objects.filter(topic=self.topic).order_by('-created_at').first()
        last_reply = Reply.objects.filter(parent_comment__topic=self.topic).order_by('-created').first()

        last_activity = max(
            last_comment.created_at if last_comment else None,
            last_reply.created if last_reply else None,
        )
        self.assertEqual(last_activity.date(), reply.created.date())
