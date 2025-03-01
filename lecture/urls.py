from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/<str:course_id>', views.lecture_home, name="lecture_home"),
    path('video/<str:video_id>',views.lecture_video,name="lecture_video_content")
  
]
