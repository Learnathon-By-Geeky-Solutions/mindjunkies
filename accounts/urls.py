from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.ProfileUpdateView.as_view(), name='edit_profile'),
]
