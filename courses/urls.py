from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('my_courses/', views.user_course_list, name='my_course_list'),
    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/', views.edit_course, name='edit_course'),


    path('<str:slug>/', views.course_details, name='course_details'),
    path('<str:course_slug>/', include('lecture.urls')),

    path('course_view/<str:slug>/', views.course_view, name='course_view'),
]
