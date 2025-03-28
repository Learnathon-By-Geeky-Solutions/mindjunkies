from django.test import TestCase
from django.contrib.auth import get_user_model
from mindjunkies.courses.models import Course, Module
from mindjunkies.forum.models import (
    ForumTopic, LikedPost, ForumComment, LikedComment, Reply, LikedReply
)

User = get_user_model()

class ForumModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.course = Course.objects.create(name="Test Course")
        self.module = Module.objects.create(name="Test Module", course=self.course)
        self.topic = ForumTopic.objects.create(
            title="Test Topic",
            content="This is a test topic.",
            author=self.user,
            course=self.course,
            module=self.module
        )
        self.comment = ForumComment.objects.create(
            topic=self.topic,
            content="This is a test comment.",
            author=self.user
        )
        self.reply = Reply.objects.create(
            author=self.user,
            parent_comment=self.comment,
            body="This is a test reply."
        )
    
    def test_forum_topic_creation(self):
        self.assertEqual(self.topic.title, "Test Topic")
        self.assertEqual(self.topic.author, self.user)
        self.assertTrue(self.topic.slug)

    def test_forum_comment_creation(self):
        self.assertEqual(self.comment.content, "This is a test comment.")
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.topic, self.topic)
    
    def test_reply_creation(self):
        self.assertEqual(self.reply.body, "This is a test reply.")
        self.assertEqual(self.reply.author, self.user)
        self.assertEqual(self.reply.parent_comment, self.comment)
    
    def test_liked_post(self):
        like = LikedPost.objects.create(topic=self.topic, user=self.user)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.topic, self.topic)
    
    def test_liked_comment(self):
        like = LikedComment.objects.create(comment=self.comment, user=self.user)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.comment, self.comment)
    
    def test_liked_reply(self):
        like = LikedReply.objects.create(reply=self.reply, user=self.user)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.reply, self.reply)
    
    def test_get_reply_count(self):
        self.assertEqual(self.topic.get_reply_count(), 1)
    
    def test_get_last_activity(self):
        self.assertEqual(self.topic.get_last_activity(), self.reply.created)
