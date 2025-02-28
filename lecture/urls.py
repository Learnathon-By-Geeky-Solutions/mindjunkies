from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/<int:course_id>/', views.lecture_home, name="lecture_home"),
  
]
