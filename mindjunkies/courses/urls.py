from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("my_courses/", views.user_course_list, name="my_course_list"),
    path("my_courses_view/", views.MyCoursesView.as_view(), name="my_courses"),
    path("new_courses/", views.NewCourseView.as_view(), name="new_course"),
    path("popular_courses/", views.PopularCoursesView.as_view(), name="popular_course"),
    path("create_course/", views.CreateCourseView.as_view(), name="create_course"),
    path("edit_course/", views.CourseUpdateView.as_view(), name="edit_course"),
    path(
        "rate/<slug:course_slug>/", views.RatingCreateView.as_view(), name="rate_course"
    ),
    path("delete/<slug:course_slug>/", views.DeleteCourseView.as_view(), name="delete_course"),
    path("<str:slug>/", views.course_details, name="course_details"),
    path("<str:course_slug>/", include("mindjunkies.lecture.urls")),
    path("<str:course_slug>/forums/", include("mindjunkies.forums.urls")),
    
]
