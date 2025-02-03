from django.urls import path
from . import views

urlpatterns = [
    path('classroom_details', views.classroom_details, name='classroom_details'),
]
