from django.urls import path

from .views import CreateLiveClassView, JoinLiveClassView, LiveClassListView

urlpatterns = [
    path("course/<str:slug>/", LiveClassListView.as_view(), name="list_live_classes"),
    path(
        "course/<str:slug>/create/",
        CreateLiveClassView.as_view(),
        name="create_live_class",
    ),
    path("<str:meeting_id>/join/", JoinLiveClassView.as_view(), name="join_live_class"),
]
