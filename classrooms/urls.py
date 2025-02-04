from django.urls import path
from . import views

urlpatterns = [
    path('classroom_details', views.classroom_details, name='classroom_details'),
    path('create_classroom',views.createClassroom,name='create_classroom')
]
