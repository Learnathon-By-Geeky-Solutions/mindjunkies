from django.urls import path
from . import views

urlpatterns = [
    path('meet-room/', views.meeting, name='meeting'),
]