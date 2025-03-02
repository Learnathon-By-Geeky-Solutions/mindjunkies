from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/<str:slug>', views.lecture_home, name="lecture_home"),
    path('video/<str:module_id>/<str:video_id>',views.lecture_video,name="lecture_video_content"),
    path('create/<str:slug>',views.create_lecture,name="create_lecture"),
    path('create/content/<str:course_slug>/<str:lecture_slug>',views.create_content,name="create_content")

   
  
]
