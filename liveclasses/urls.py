from django.urls import path
from .views import list_live_classes, create_live_class, join_live_class

urlpatterns = [
    path("course/<str:slug>/", list_live_classes, name="list_live_classes"),
    path("course/<str:slug>/create/", create_live_class, name="create_live_class"),
    path("<str:meeting_id>/join/", join_live_class, name="join_live_class"),
]
