from django.urls import path
from . import views

urlpatterns = [
    path('course_details/<str:slug>/', views.course_details, name='course_details'),
    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/', views.edit_course, name='edit_course'),
    path('my_courses/', views.user_course_list, name='my_course_list'),
    path('courses/', views.course_list, name='course_list'),
]
