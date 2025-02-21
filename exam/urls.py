from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
   
    path('home', views.exam_home, name='exam_home'),
]