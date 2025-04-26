from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from mindjunkies.courses.models import Course, Module
from mindjunkies.forums.models import ForumTopic, ForumComment, Reply, LikedPost, LikedComment, LikedReply
from datetime import datetime

User = get_user_model()

class ForumModelsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

        # Create test course and module
        self.course = Course.objects.create(
            title="Test Course",
            short_introduction="This is a short intro.",
            course_description="Detailed description of the course.",
            teacher=self.user,
            slug="test-course",
        )
        self.module = Module.objects.create(
            course=self.course,
            details="Test module details",
            title='Test Module'
            
        )

        # Create test forum topic
        self.topic = ForumTopic.objects.create(
            title='Test Topic',
            content='This is a test topic',
            author=self.user,
            course=self.course,
            module=self.module
        )

        # Create test forum comment
        self.comment = ForumComment.objects.create(
            topic=self.topic,
            content='This is a test comment',
            author=self.user
        )

        # Create test reply
        self.reply = Reply.objects.create(
            author=self.user,
            parent_comment=self.comment,
            body='This is a test reply'
        )

    def test_forum_topic_creation(self):
        """Test ForumTopic model creation and attributes"""
        self.assertEqual(self.topic.title, 'Test Topic')
        self.assertEqual(self.topic.slug, slugify('Test Topic'))
        self.assertEqual(self.topic.content, 'This is a test topic')
        self.assertEqual(self.topic.author, self.user)
        self.assertEqual(self.topic.course, self.course)
        self.assertEqual(self.topic.module, self.module)
        self.assertIsInstance(self.topic.created_at, datetime)
        self.assertIsInstance(self.topic.updated_at, datetime)
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_forum_topic_save_slug(self):
        """Test ForumTopic slug generation on save"""
        topic = ForumTopic.objects.create(
            title='Another Test Topic',
            content='Another test',
            author=self.user,
            course=self.course,
            module=self.module
        )
        self.assertEqual(topic.slug, slugify('Another Test Topic'))

    def test_forum_topic_get_reply_count(self):
        """Test ForumTopic get_reply_count method"""
        ForumComment.objects.create(
            topic=self.topic,
            content='Another comment',
            author=self.user
        )
          # Two comments

    def test_forum_topic_get_last_activity(self):
        """Test ForumTopic get_last_activity method"""
        comment2 = ForumComment.objects.create(
            topic=self.topic,
            content='Newer comment',
            author=self.user
        )
        last_activity = self.topic.get_last_activity()
        self.assertEqual(last_activity, comment2.created_at)

    def test_liked_post_creation(self):
        """Test LikedPost model creation"""
        liked_post = LikedPost.objects.create(
            topic=self.topic,
            user=self.user2
        )
        self.assertEqual(liked_post.topic, self.topic)
        self.assertEqual(liked_post.user, self.user2)
        self.assertIsInstance(liked_post.created, datetime)
        self.assertEqual(
            str(liked_post),
            f"{self.user2.username} : {self.topic.content[:30]}"
        )

    def test_forum_comment_creation(self):
        """Test ForumComment model creation"""
        self.assertEqual(self.comment.topic, self.topic)
        self.assertEqual(self.comment.content, 'This is a test comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertIsInstance(self.comment.created_at, datetime)
        self.assertIsInstance(self.comment.updated_at, datetime)
        self.assertEqual(
            str(self.comment),
            f"Reply by {self.user.username} on {self.topic.title}"
        )

    def test_liked_comment_creation(self):
        """Test LikedComment model creation"""
        liked_comment = LikedComment.objects.create(
            comment=self.comment,
            user=self.user2
        )
        self.assertEqual(liked_comment.comment, self.comment)
        self.assertEqual(liked_comment.user, self.user2)
        self.assertIsInstance(liked_comment.created, datetime)
       

    def test_reply_creation(self):
        """Test Reply model creation"""
        self.assertEqual(self.reply.author, self.user)
        self.assertEqual(self.reply.parent_comment, self.comment)
        self.assertEqual(self.reply.body, 'This is a test reply')
        self.assertIsInstance(self.reply.created, datetime)
       

    def test_reply_to_reply(self):
        """Test Reply to another reply"""
        child_reply = Reply.objects.create(
            author=self.user2,
            parent_reply=self.reply,
            body='This is a nested reply'
        )
        self.assertEqual(child_reply.parent_reply, self.reply)
        self.assertIsNone(child_reply.parent_comment)
        self.assertEqual(child_reply.body, 'This is a nested reply')

    def test_liked_reply_creation(self):
        """Test LikedReply model creation"""
        liked_reply = LikedReply.objects.create(
            reply=self.reply,
            user=self.user2
        )
        self.assertEqual(liked_reply.reply, self.reply)
        self.assertEqual(liked_reply.user, self.user2)
        self.assertIsInstance(liked_reply.created, datetime)
        self.assertEqual(
            str(liked_reply),
            f"{self.user2.username} : {self.reply.body[:30]}"
        )

    def test_forum_topic_ordering(self):
        """Test ForumTopic Meta ordering"""
        topic2 = ForumTopic.objects.create(
            title='Second Topic',
            content='Second test',
            author=self.user,
            course=self.course,
            module=self.module
        )
        topics = ForumTopic.objects.all()
        self.assertEqual(topics[0], topic2)  # Newer topic first

    def test_forum_comment_ordering(self):
        """Test ForumComment Meta ordering"""
        comment2 = ForumComment.objects.create(
            topic=self.topic,
            content='Second comment',
            author=self.user
        )
        comments = ForumComment.objects.all()
        self.assertEqual(comments[0], self.comment)  # Older comment first

    def test_reply_ordering(self):
        """Test Reply Meta ordering"""
        reply2 = Reply.objects.create(
            author=self.user,
            parent_comment=self.comment,
            body='Second reply'
        )
        replies = Reply.objects.all()
        self.assertEqual(replies[0], self.reply)  # Older reply first