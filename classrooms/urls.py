from django.urls import path
from . import views

urlpatterns = [
    path('classroom_details/<str:slug>', views.classroom_details, name='classroom_details'),
    path('create_classroom',views.createClassroom,name='create_classroom'),
    path('edit_classroom', views.edit_classroom, name='edit_classroom')
]
