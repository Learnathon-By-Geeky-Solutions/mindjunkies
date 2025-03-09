from django.urls import path, include
from . import views
urlpatterns=[
    path("home",views.ForumHomeView.as_view(),name="forum_home")
]