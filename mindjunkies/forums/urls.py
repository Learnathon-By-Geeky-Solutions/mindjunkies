from django.urls import path

from . import views

urlpatterns = [path("home", views.ForumHomeView.as_view(), name="forum_home"),
               path("<str:module_id>/thread",views.ForumThreadView.as_view(),name="forum_thread"),
               path("<str:module_id>/thread/submit",views.TopicSubmissionView.as_view(),name="forum_submission"),
               path("<str:topic_slug>/thread/details",views.ForumThreadDetailsView.as_view(),name="forum_thread_details")
               
               ]
