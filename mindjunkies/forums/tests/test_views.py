from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from mindjunkies.courses.models import Course, Module
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
    def setUp(self):
        self.client = Client()
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
       
        
        # Create a Course with a teacher
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
            module=self.module
        )
        
        self.comment = ForumComment.objects.create(
            topic=self.topic,
            content='Test comment',
            author=self.user
        )
        
        self.reply = Reply.objects.create(
            parent_comment=self.comment,
            body='Test reply',
            author=self.user
        )
  

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