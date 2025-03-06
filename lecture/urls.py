from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.lecture_home, name="lecture_home"),
    path('create/module/', views.create_module, name='create_module'),
    path('create/lecture/', views.create_lecture, name="create_lecture"),
    path('edit/<str:lecture_slug>', views.edit_lecture, name="edit_lecture"),
    path('create/<str:lecture_slug>/content/<str:type>', views.create_content, name="create_content"),

    # HLS video streaming
    path('serve_hls_playlist/<str:video_id>/', views.serve_hls_playlist, name='serve_hls_playlist'),
    path('serve_hls_segment/<str:video_id>/<str:segment_name>/', views.serve_hls_segment, name='serve_hls_segment'),
    path('video/<str:module_id>/<str:video_id>', views.lecture_video, name="lecture_video_content"),

]
