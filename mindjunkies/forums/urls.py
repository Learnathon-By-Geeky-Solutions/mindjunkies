from django.urls import path

from . import views

urlpatterns = [
    path("<str:course_slug>/home", views.ForumHomeView.as_view(), name="forum_home"),
    path(
        "<str:course_slug>/<str:module_id>/thread",
        views.ForumThreadView.as_view(),
        name="forum_thread",
    ),
    path(
        "<str:course_slug>/<str:module_id>/thread/submit",
        views.TopicSubmissionView.as_view(),
        name="forum_submission",
    ),
    path(
        "<str:course_slug>/<str:module_id>/<str:topic_id>/update",
        views.TopicUpdateView.as_view(),
        name="forum_update",
    ),
    path(
        "<str:course_slug>/<str:module_id>/<str:topic_id>/thread/details",
        views.ForumThreadDetailsView.as_view(),
        name="forum_thread_details",
    ),
    path(
        "<str:course_slug>/<str:module_id>/<str:topic_id>/thread/comment",
        views.CommentSubmissionView.as_view(),
        name="forum_thread_comment",
    ),
    path(
        "<str:course_slug>/<str:module_id>/<str:topic_id>/<str:comment_id>/thread/reply",
        views.ReplySubmissionView.as_view(),
        name="forum_thread_reply",
    ),
    path(
        "<int:reply_id>/thread/reply-form",
        views.ReplyFormView.as_view(),
        name="reply_form",
    ),
    path("<str:pk>/liked_post", views.LikePostView.as_view(), name="liked_post"),
    path(
        "<str:pk>/liked_comment", views.LikeCommentView.as_view(), name="liked_comment"
    ),
    path("<str:pk>/liked_reply", views.LikeReplyView.as_view(), name="liked_reply"),
    path(
        "<str:course_slug>/<str:module_id>/<str:topic_id>/deltopic",
        views.TopicDeletionView.as_view(),
        name="delete_topic",
    ),
    path(
        "delcomment/<str:course_slug>/<str:module_id>/<str:topic_id>/<str:comment_id>",
        views.CommentDeletionView.as_view(),
        name="delete_comment",
    ),
    path(
        "delreply/<str:course_slug>/<str:module_id>/<str:topic_id>/<str:reply_id>",
        views.ReplyDeletionView.as_view(),
        name="delete_reply",
    ),
]
