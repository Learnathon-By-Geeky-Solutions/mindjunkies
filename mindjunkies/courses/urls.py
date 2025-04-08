from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("my_courses/", views.user_course_list, name="my_course_list"),
    path("create_course/", views.CreateCourseView.as_view(), name="create_course"),
    path("edit_course/", views.CourseUpdateView.as_view(), name="edit_course"),

    path('create-course-token/<slug:slug>/', views.CreateCourseTokenView.as_view(), name='create_course_token'),

    path("<str:slug>/", views.course_details, name="course_details"),
    path("<str:course_slug>/", include("mindjunkies.lecture.urls")),
    path("<str:course_slug>/forums/", include("mindjunkies.forums.urls")),
]
