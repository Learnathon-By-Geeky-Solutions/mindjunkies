from django.urls import path
from .views import *

urlpatterns = [
    # Add your URL patterns here
    path('content/', content_list, name='content'),
]