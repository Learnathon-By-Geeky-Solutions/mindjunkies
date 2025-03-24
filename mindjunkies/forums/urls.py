from django.urls import path

from . import views

urlpatterns = [path("<str:course_slug>/home", views.ForumHomeView.as_view(), name="forum_home"),
               path("<str:course_slug>/<str:module_id>/thread",views.ForumThreadView.as_view(),name="forum_thread"),
               path("<str:course_slug>/<str:module_id>/thread/submit",views.TopicSubmissionView.as_view(),name="forum_submission"),
               path("<str:course_slug>/<str:topic_slug>/thread/details",views.ForumThreadDetailsView.as_view(),name="forum_thread_details"),
               path("<str:course_slug>/<str:topic_slug>/thread/comment",views.CommentSubmissionView.as_view(),name="forum_thread_comment"),
               path("<str:course_slug>/<str:topic_slug>/<str:comment_id>/thread/reply",views.ReplySubmissionView.as_view(),name="forum_thread_reply"),
               path("<int:reply_id>/thread/reply-form",views.ReplyFormView.as_view(),name="reply_form")
            
            
               ]
