from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/<str:slug>', views.lecture_home, name="lecture_home"),
     path('serve_hls_playlist/<str:video_id>/', views.serve_hls_playlist, name='serve_hls_playlist'),
    path('video/<str:module_id>/<str:video_id>',views.lecture_video,name="lecture_video_content"),
    path('create/<str:course_slug>',views.create_lecture,name="create_lecture"),
    path('create/content/<str:course_slug>/<str:lecture_slug>/<str:type>',views.create_content,name="create_content"),
    path('edit/<str:course_slug>/<str:lecture_slug>',views.edit_lecture,name="edit_lecture"),
    path('create/module/<str:course_slug>',views.create_module,name='create_module'),

   
  
]
