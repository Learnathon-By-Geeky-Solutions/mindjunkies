from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from mindjunkies.courses.models import Course, Module
from mindjunkies.forums.models import ForumTopic, ForumComment, Reply

User = get_user_model()

class ForumViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(title='Test Course', slug='test-course')
        self.module = Module.objects.create(title='Test Module', course=self.course)
        self.forum_topic = ForumTopic.objects.create(
            title='Test Topic', slug='test-topic', course=self.course, author=self.user
        )
        self.comment = ForumComment.objects.create(topic=self.forum_topic, author=self.user, content='Test Comment')
        self.reply = Reply.objects.create(parent_comment=self.comment, author=self.user, body='Test Reply')

    def test_forum_home_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('forum_home', kwargs={'course_slug': self.course.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/forum_home.html')

    def test_forum_thread_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('forum_thread', kwargs={'course_slug': self.course.slug, 'module_id': self.module.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/forum_threads.html')

    def test_forum_thread_details_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('forum_thread_details', kwargs={'course_slug': self.course.slug, 'topic_slug': self.forum_topic.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forums/forum_thread_details.html')

    def test_topic_submission_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('topic_submission', kwargs={'course_slug': self.course.slug, 'module_id': self.module.id}), {
            'title': 'New Test Topic', 'content': 'Topic content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ForumTopic.objects.filter(title='New Test Topic').exists())

    def test_comment_submission_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('comment_submission', kwargs={'course_slug': self.course.slug, 'topic_slug': self.forum_topic.slug}), {
            'content': 'New Test Comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ForumComment.objects.filter(content='New Test Comment').exists())

    def test_reply_submission_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('reply_submission', kwargs={'course_slug': self.course.slug, 'topic_slug': self.forum_topic.slug, 'comment_id': self.comment.id}), {
            'body': 'New Test Reply'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reply.objects.filter(body='New Test Reply').exists())

    def test_like_post_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('like_post', kwargs={'pk': self.forum_topic.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.forum_topic.likes.filter(id=self.user.id).exists())

    def test_like_comment_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('like_comment', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.comment.likes.filter(id=self.user.id).exists())

    def test_like_reply_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('like_reply', kwargs={'pk': self.reply.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.reply.likes.filter(id=self.user.id).exists())
