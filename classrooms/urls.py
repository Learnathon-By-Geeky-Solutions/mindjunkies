from django.urls import path
from . import views

urlpatterns = [
    path('classroom_details/<str:slug>/', views.classroom_details, name='classroom_details'),
    path('create_classroom/', views.create_classroom,name='create_classroom'),
    path('edit_classroom/', views.edit_classroom, name='edit_classroom'),
    path('my_classrooms/', views.user_classroom_list, name='my_classroom_list'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
]
