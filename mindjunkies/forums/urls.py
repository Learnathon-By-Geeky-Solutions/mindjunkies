from django.urls import path

from . import views

urlpatterns = [path("home", views.ForumHomeView.as_view(), name="forum_home"),
               path("thread",views.ForumThreadView.as_view(),name="forum_thread"),
               path("thread/details",views.ForumThreadDetailsView.as_view(),name="forum_thread_details")
               
               ]
