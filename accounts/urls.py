from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
