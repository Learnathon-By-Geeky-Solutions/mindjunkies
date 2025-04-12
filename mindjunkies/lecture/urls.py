from django.urls import path

from . import views

urlpatterns = [
    path("home", views.LectureHomeView.as_view(), name="lecture_home"),
    path("module/create", views.CreateModuleView.as_view(), name="create_module"),
    path(
        "<int:module_id>/lecture/create",
        views.CreateLectureView.as_view(),
        name="create_lecture",
    ),
    path(
        "edit/<str:lecture_slug>", views.EditLectureView.as_view(), name="edit_lecture"
    ),
    path(
        "create/<str:lecture_slug>/content/<str:format>",
        views.CreateContentView.as_view(),
        name="create_content",
    ),
    path(
        "video/<str:module_id>/<str:video_id>",
        views.lecture_video,
        name="lecture_video_content",
    ),
]
